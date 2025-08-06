import requests
import base64
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad



def decrypt_response(response_text: str) -> str:
    def aes_decrypt(cipher_bytes: bytes, aes_key: bytes) -> bytes:
        return unpad(AES.new(aes_key, AES.MODE_ECB).decrypt(cipher_bytes), AES.block_size)

    s = hashlib.sha1("tSdGtmwh49BcR1irt18mxG41dGsBuGKS".encode())
    key_hex = s.hexdigest()[:32]
    print(key_hex)
    cipher_bytes = base64.b64decode(response_text)
    res = aes_decrypt(cipher_bytes=cipher_bytes, aes_key=bytes.fromhex(key_hex)).decode()
    return res



headers = {
    "accept": "*/*",
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
url = "https://api.weibotop.cn/currentitems"
response = requests.get(url, headers=headers)

res = decrypt_response(response.text)
print(res)


