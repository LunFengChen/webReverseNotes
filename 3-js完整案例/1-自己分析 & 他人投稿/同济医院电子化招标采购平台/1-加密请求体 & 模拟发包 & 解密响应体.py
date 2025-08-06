import random

import requests
import json
import base64

from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

from loguru import logger


def rsa_ecb_encrypt(plain_bytes: bytes, public_key_b64: str) -> bytes:
    public_key_pem = base64.b64decode(public_key_b64)
    public_key = RSA.importKey(public_key_pem)

    cipher = PKCS1_v1_5.new(public_key)
    ciphertext = cipher.encrypt(plain_bytes)

    return ciphertext


def aes_ecb_encrypt(plain_bytes: bytes, aes_key: bytes) -> bytes:
    return AES.new(aes_key, AES.MODE_ECB).encrypt(pad(plain_bytes, AES.block_size))


url = "https://zbb.tjhonline.com.cn/tjh/purchaser/public/frontPageAnnouncementList"

aesKey = "".join(random.sample("0123456789abcdef", 16)).upper()
public_key_b64 = "MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQCC3Lb0O4zgEakDfJ4XJO5zadXep9bQeWyJ6pa0e328PYQYZgLNP7eVrAP7mVZgG+8D4MicIcStTQnBxF8AEyJKrh/M/3WSSK2zDvrZn1paWf4SA8zFIn5cuYlcUH+WuxghQn3kKRUW2qtBY9eaGF5qntascctNgQTHmW3eqQzDBQIDAQAB"
aesKey_rsa_b64 = base64.b64encode(rsa_ecb_encrypt(aesKey.encode(), public_key_b64)).decode()
logger.info(f"aeskey: {aesKey} -> rsa加密 -> aesKey_rsa: {aesKey_rsa_b64}")

content_dct = {"noticeName": "医院", "pageNum": 1, "pageSize": 10, "tenderCategory": "1", "noticeTypeList": None,
               "tenderClass": None}
content_str = json.dumps(content_dct, separators=(',', ':'))
content_b64 = base64.b64encode(aes_ecb_encrypt(content_str.encode(), aesKey.encode())).decode()
logger.info(f"content_dct: {content_dct} -> aes/cbc处理, aesKey: {aesKey} -> content_b64: {content_b64}")

headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Connection": "keep-alive",
    "Content-Type": "application/json;charset=UTF-8",
    "Origin": "https://zbb.tjhonline.com.cn",
    "Referer": "https://zbb.tjhonline.com.cn/homeNotice",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Google Chrome\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
headers["aesKey"] = aesKey

cookies = {
    "sidebarStatus": "0"
}
data = {
    "content": content_b64,
    "aesKey": aesKey_rsa_b64
}

data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, data=data)

logger.success(response.json())

def rsa_ecb_decrypt(cipherd_bytes: bytes, private_key_b64: str) -> bytes:
    private_key_pem = base64.b64decode(private_key_b64)
    private_key = RSA.import_key(private_key_pem)
    cipher = PKCS1_v1_5.new(private_key)
    decrypted_bytes = cipher.decrypt(cipherd_bytes, Random.new().read(16))
    return decrypted_bytes

def aes_ecb_decrypt(cipher_bytes: bytes, aes_key: bytes) -> bytes:
    return unpad(AES.new(aes_key, AES.MODE_ECB).decrypt(cipher_bytes), AES.block_size)



private_key_b64 = "MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBALROqKeWuu+G6z6V7lesaAIC8FWWJ8qYRRy4HbbakJBH+OEWfD+0/MmMnZ28aMiV3qDy34SLfddDxvWJo/SR8iL8bjeqOEQxenu8Ogec+290w4F8IW6Ips/kZ5pnkg/TUn1GATOSV+RbB90okuykbBEbGKaNqGczJ/lI7RpfNvCpAgMBAAECgYA9RzJYaoizmRXgGlJ7Z3Odo2QMolB5sRBj90rZ9yQEdQFndh3aBOeYk/qJPhwad5zG9GP0hvfIrhczIYkgOG2i1ZvBAFBP7IZiGJz5PxS9QOFPg926sI6Mv3nBIS0+U88IyzPL/fQWNvhc3b9Y95kYp4p0Wk4zzNe9HNNUMQHdUQJBAOwA6EoVSlxlpNivoAGrMynLlnHmZ7fEpXXQINUbhpX8+I3fazoWcRaYpfLmVKa82DJXHUe8URFX3oir3kAocVUCQQDDlahWFmYmtNYqLitJdIdltTcmQtAgHlfshdYnq6Gg8jSjwh40sXF8MgZfG03+sfdmKbSG3e+7Ihb/X5P/odIFAkEAlz3Rn0BbojDlXpPWN5uOMzesFxwv1Z3o50JU+B0mt9IhO1I1dklRecijeLFRCHW3GzOmqQUu8q1cCDwUNwtz7QJBAJ3BT8coR/q+b+QT20xjVnaeBT6yM2dEskyP4x2aXUMROY5Am9aKrWuseeEqh+2ApHld+EO0LZJ2O7B96kUNw/UCQHhXTTBHc2HkyU84U2+OAB2hJtJBmj+eGl0iqNfOq3JyiIemC/bV74sASLa+NN9CJRotBh9jzmzNpwEi24Y8KHE="
# aesKey_rsa_b64 = "Q/uFqGTp/n8KbtLEb+Kh8lXhg1R2sIidUfe0A4mxRUkTKg9xiMUSfdy+cwoowRLoqR+J2xfZt9Vaawyg672MkXIIxVn4Cl/8L8c43fztUhtAiYm3lTuzMK7gS1+pY5Ipcnye/+D3tMjRYNoC3WqL3wRn68w83MbJpUh7HlahAdI="
aesKey_rsa_b64 = response.json()["aesKey"]
aesKey = rsa_ecb_decrypt(base64.b64decode(aesKey_rsa_b64), private_key_b64).decode()
content_aes_b64 = response.json()["content"]
res = aes_ecb_decrypt(base64.b64decode(content_aes_b64.encode()), aesKey.encode()).decode()

logger.success(f"解密响应体为: {res}")