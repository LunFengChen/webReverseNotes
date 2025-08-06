import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad


def decrypt(cipher_bytes: bytes) -> bytes:
    # (1) 这里直接去找到对象，控制台.toString()拿到的一定是正确的，静态代码找到不一定对
    key_bytes = bytes.fromhex("4474386a39774777253648627866466e")
    # (2) 也可以直接调用函数转
    # key_bytes = int_list_to_bytes([1148467306, 964118391, 624314466, 2019968622])
    iv_bytes = bytes.fromhex("30313233343536373839414243444546")

    cipher = AES.new(key_bytes, AES.MODE_CBC, iv_bytes)
    return unpad(cipher.decrypt(cipher_bytes), AES.block_size)


headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Referer": "https://jzsc.mohurd.gov.cn/data/company",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    "accessToken;": "",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "timeout": "30000",
    "v": "231012"
}
cookies = {
    "Hm_lvt_b1b4b9ea61b6f1627192160766a9c55c": "1753813990",
    "Hm_lpvt_b1b4b9ea61b6f1627192160766a9c55c": "1753813990",
    "HMACCOUNT": "18AD7409F43AD3B3"
}
url = "https://jzsc.mohurd.gov.cn/APi/webApi/dataservice/query/comp/list"
params = {
    "pg": "9",
    "pgsz": "15",
    "total": "450"
}
response = requests.get(
    url,
    headers=headers,
    # cookies=cookies,
    params=params
)

print(response.text)
res = decrypt(bytes.fromhex(response.text)).decode()
print(res)
