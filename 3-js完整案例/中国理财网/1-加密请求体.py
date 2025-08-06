import base64

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def aes_encrypt(plain_bytes: bytes, aes_key: bytes, aes_iv: bytes) -> bytes:
    return AES.new(aes_key, AES.MODE_CBC, aes_iv).encrypt(pad(plain_bytes, AES.block_size))


def encrtpt_request_body(plain_text: str) -> str:
    aes_key = bytes.fromhex("6257384a633633557a3749314e355239")
    aes_iv = bytes.fromhex("30303030303030303030303030303030")
    return base64.b64encode(aes_encrypt(plain_text.encode(), aes_key, aes_iv)).decode()

request_body = """{"header":{"sendSysname":"fis","msgType":"financial-products","msgId":"fp123","sendTime":"2025/7/30 15:11:02","exts":{"signature":"kXMYfwkYy49d3kBRkaIZstv07XxAFp4GZtIpO7j/U1dgPW90KnLrTmcq4OKPY6jX+MigJPylCtBKw5q8gfWNYyXhZkuP5LgKrLQrKPk6OoRseiNQPYX6Ptug1xlwcH8M0Aw3UqKuDaVpIJl1tHtdusAIzB3OiCRq3vwc05ZAtMNELAwHznOjBrS+x+7nsxG2YgFgxKb6el3npBoqh2YGIXaognSItRcNUUP1dPpIPm4h6Osx8b07NzJvTvU0ZZCJVxn+IOtzNQi5p88Efg8Y7H+kmiUO2hqqsEsdfIRiIVO+26ki9DNBbQSZ7HyV9/GNsNHbOdu/T7eQ46SIytB5bA=="}},"body":{"version":"1.0.0","trnsType":"financial-products","trnsId":"fp123","exts":{"orgName":"","prodName":"","prodRegCode":"","pageNum":4,"pageSize":20,"prodStatus":"","prodSpclAttr":"","prodInvestNature":"","prodOperateMode":"","prodRiskLevel":"","prodTermCode":"","actDaysStart":null,"actDaysEnd":null}}}"""
print(encrtpt_request_body(request_body))