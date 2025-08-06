import hashlib
import random
import string
import time

import requests
import json

cookies = {
    "_horizon_uid": "90ef4ad2-3b96-433c-a425-ad1d570d32f1"
}
url = "https://ygp.gdzwfw.gov.cn/ggzy-portal/search/v2/items"
data = {
    "type": "trading-type",
    "openConvert": False,
    "keyword": "",
    "siteCode": "44",
    "secondType": "A",
    "tradingProcess": "",
    "thirdType": "[]",
    "projectType": "",
    "publishStartTime": "",
    "publishEndTime": "",
    "pageNo": 12,
    "pageSize": 10
}
headers = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/json",
    "Origin": "https://ygp.gdzwfw.gov.cn",
    "Referer": "https://ygp.gdzwfw.gov.cn/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "X-Dgi-Req-App": "ggzy-portal",
    "X-Dgi-Req-Nonce": "".join(random.sample(string.ascii_letters+string.digits, 16)),
    # "X-Dgi-Req-Signature": "fe55764c7480f5a1fbf01253c9c224ac8b122fe16c150eab2c6deb1f2332f917",
    "X-Dgi-Req-Timestamp": str(int(time.time()*1000)),
}

data_string = "&".join(f"{k}={v}" for k, v in sorted(data.items(), key=lambda item: item[0]))

def calc_sign(nonce_string: str, timestamp_ms_string: str, body_string: str):
    salt_string = "k8tUyS$m"
    sign_original_string = f"{nonce_string}{salt_string}{body_string}{timestamp_ms_string}"
    return hashlib.sha256(sign_original_string.encode()).hexdigest()

headers["X-Dgi-Req-Signature"] = calc_sign(headers["X-Dgi-Req-Nonce"], headers["X-Dgi-Req-Timestamp"], data_string)
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, data=data)

print(response.text)
print(response)
