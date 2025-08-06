import requests
import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def aes_encrypt(plain_bytes: bytes, aes_key: bytes, aes_iv: bytes) -> bytes:
    return AES.new(aes_key, AES.MODE_CBC, aes_iv).encrypt(pad(plain_bytes, AES.block_size))


def encrypt_request_body(plain_text: str) -> str:
    aes_key = bytes.fromhex("6257384a633633557a3749314e355239")
    aes_iv = bytes.fromhex("30303030303030303030303030303030")
    return base64.b64encode(aes_encrypt(plain_text.encode(), aes_key, aes_iv)).decode()

cookies = {
    'size': 'default',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Connection': 'keep-alive',
    'Content-Type': 'application/cnap-message',
    'Origin': 'https://xinxipilu.chinawealth.com.cn',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0',
    'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'size=default',
}
request_body = """{"header":{"sendSysname":"fis","msgType":"financial-products","msgId":"fp123","sendTime":"2025/7/30 15:11:02","exts":{"signature":"kXMYfwkYy49d3kBRkaIZstv07XxAFp4GZtIpO7j/U1dgPW90KnLrTmcq4OKPY6jX+MigJPylCtBKw5q8gfWNYyXhZkuP5LgKrLQrKPk6OoRseiNQPYX6Ptug1xlwcH8M0Aw3UqKuDaVpIJl1tHtdusAIzB3OiCRq3vwc05ZAtMNELAwHznOjBrS+x+7nsxG2YgFgxKb6el3npBoqh2YGIXaognSItRcNUUP1dPpIPm4h6Osx8b07NzJvTvU0ZZCJVxn+IOtzNQi5p88Efg8Y7H+kmiUO2hqqsEsdfIRiIVO+26ki9DNBbQSZ7HyV9/GNsNHbOdu/T7eQ46SIytB5bA=="}},"body":{"version":"1.0.0","trnsType":"financial-products","trnsId":"fp123","exts":{"orgName":"","prodName":"","prodRegCode":"","pageNum":4,"pageSize":20,"prodStatus":"","prodSpclAttr":"","prodInvestNature":"","prodOperateMode":"","prodRiskLevel":"","prodTermCode":"","actDaysStart":null,"actDaysEnd":null}}}"""

response = requests.post(
    'https://xinxipilu.chinawealth.com.cn/platformApi/lcxp-platService/product/getProductList',
    cookies=cookies,
    headers=headers,
    data=encrypt_request_body(request_body),
)
print(response.text)
print(response)