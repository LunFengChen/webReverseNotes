import json

import requests
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

def encrypt_time(plain_text: str) -> str:
    def aes_encrypt(plain_bytes: bytes, aes_key: bytes) -> bytes:
        return AES.new(aes_key, AES.MODE_ECB).encrypt(pad(plain_bytes, AES.block_size))

    s = hashlib.sha1("tSdGtmwh49BcR1irt18mxG41dGsBuGKS".encode())
    key_hex = s.hexdigest()[:32]
    cipher_bytes = aes_encrypt(plain_bytes=plain_text.encode(), aes_key=bytes.fromhex(key_hex))
    return base64.b64encode(cipher_bytes).decode()


def decrypt_response(response_text: str) -> str:
    def aes_decrypt(cipher_bytes: bytes, aes_key: bytes) -> bytes:
        return unpad(AES.new(aes_key, AES.MODE_ECB).decrypt(cipher_bytes), AES.block_size)

    s = hashlib.sha1("tSdGtmwh49BcR1irt18mxG41dGsBuGKS".encode())
    key_hex = s.hexdigest()[:32]
    cipher_bytes = base64.b64decode(response_text)
    res = aes_decrypt(cipher_bytes=cipher_bytes, aes_key=bytes.fromhex(key_hex)).decode()
    return res


headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "origin": "https://www.weibotop.cn",
    "priority": "u=1, i",
    "referer": "https://www.weibotop.cn/",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
}
url = "https://api.weibotop.cn/getclosesttime"
params = {
    "timestamp": encrypt_time("2025-07-26T01:24:04")
}
response = requests.get(url, headers=headers, params=params)
timeid = response.json()[0]  # 第一个元素就是timeid
print(timeid)

url = "https://api.weibotop.cn/currentitems"
response = requests.get(url, headers=headers, params={"timeid": encrypt_time(timeid)})

res = decrypt_response(response.text)
print(res)
