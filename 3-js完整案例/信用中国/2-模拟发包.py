import subprocess
import time
import uuid
from functools import partial

subprocess.Popen = partial(subprocess.Popen, encoding="utf-8")
import execjs


import requests
import base64


def generate_nonceStr() -> str:
    return str(uuid.uuid4()).replace("-", "")


def generate_timestamp_ms() -> str:
    return str(int(time.time() * 1000))


page = 3
with open('3-sm2签名.js', 'r', encoding='utf-8') as f:
    js = f.read()
ctx = execjs.compile(js)
result = ctx.call('encrypt', page, generate_nonceStr())
print(result)

cookies = {
    '_gscu_2016493642': '47213795wc8hnu87',
    '_gscbrs_2016493642': '1',
    '_gscs_2016493642': '47213795l4a6ru87|pv:1',
}

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'C-GATEWAY-QUERY-ENCRYPT': '1',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Referer': 'https://credit.hd.gov.cn/xyxxgs/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0',
    'sec-ch-ua': '"Chromium";v="136", "Microsoft Edge";v="136", "Not.A/Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'x-gateway-body': 'blob',
    # 'Cookie': '_gscu_2016493642=47213795wc8hnu87; _gscbrs_2016493642=1; _gscs_2016493642=47213795l4a6ru87|pv:1',
}

response = requests.get(
    f'https://credit.hd.gov.cn/zx_website/website/sgs/xzcffr?version=1.0&appId=27IGtFrNFDc&signType=SM2&encryptType=SM4&nonceStr={result.get("nonce")}&timestamp={result.get("timestamp")}&queryContent={result.get("queryContent")}&sign={result.get("sign")}',
    cookies=cookies,
    headers=headers,
)
encoded_bytes = base64.b64encode(response.content)
# 将 Base64 字节转换为字符串
encoded_str = encoded_bytes.decode('utf-8')

with open('4-扣sm4解密代码.js', 'r', encoding='utf-8') as f:
    js = f.read()
ctx1 = execjs.compile(js)
print(ctx1.call('decryptfrombase64', encoded_str))