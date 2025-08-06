import hashlib

import requests
import json

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "baggage": "sentry-environment=production,sentry-release=global-sso%401.0.56,sentry-public_key=3ed0768cf835395f20e8c3bca4499ed8,sentry-trace_id=5513b4b3b5a542b69deb9d0e2fa64142",
    "content-type": "application/json",
    "dev-info": "dzGrysHeguf5MAl0cN9t",
    "dev-info-bs": "CH67Y1Z2WdJFzSEUrI4J-FrB030ve9huJ2f1Ho3Doke1ExykraAVWya1_lPmqIy5VTqJzrvknU-FHVViEeD7CuxhcymrCHJTCRX4l8cz9HlfWW28ZjXABBuSh71bCVKgUgepp99flp89O1La22U6PUX0XvaxvgH7",
    "lang": "zh-CN",
    "origin": "https://global.lianlianpay.com",
    "priority": "u=1, i",
    "referer": "https://global.lianlianpay.com/signin?from=global",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "sentry-trace": "5513b4b3b5a542b69deb9d0e2fa64142-a5e4ef787bad570b-1",
    "source": "PC",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
}
cookies = {
    "sajssdk_2015_cross_new_user": "1",
    "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%221985ecaa94f1029-0b69fb5d5704d88-4c657b58-2304000-1985ecaa9501ac1%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_landing_page%22%3A%22https%3A%2F%2Fglobal.lianlianpay.com%2Fsignin%3Ffrom%3Dglobal%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk4NWVjYWE5NGYxMDI5LTBiNjlmYjVkNTcwNGQ4OC00YzY1N2I1OC0yMzA0MDAwLTE5ODVlY2FhOTUwMWFjMSJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%221985ecaa94f1029-0b69fb5d5704d88-4c657b58-2304000-1985ecaa9501ac1%22%7D",
    "BSFIT_DFPUUID": "EADWzTm8lYcdupDRa-j6PG7i03fsKryb",
    "BSFIT_EXPIRATION": "1753980927766",
    "BSFIT_COOKIE_CACHE": "F4PFlvPo9qOV-Ol_I9QzSxO4HT0TSixS",
    "BSFIT_DEVICEID": "CH67Y1Z2WdJFzSEUrI4J-FrB030ve9huJ2f1Ho3Doke1ExykraAVWya1_lPmqIy5VTqJzrvknU-FHVViEeD7CuxhcymrCHJTCRX4l8cz9HlfWW28ZjXABBuSh71bCVKgUgepp99flp89O1La22U6PUX0XvaxvgH7",
    "_vid_t": "Nq0tKlCveQLal8sD+pDNSAv5t8STuGIJvpVi4xYgktyfx4B7Q6GKFTvQ3xMYzbna0ht2HTitCT9bPw=="
}
url = "https://global.lianlianpay.com/cb-va-sso-api/login"
data = {
    "loginName": "13111111111",
    "password": hashlib.md5(hashlib.md5("111111".encode()).hexdigest().encode()).hexdigest()
}
print(data)
data = json.dumps(data, separators=(',', ':'))
response = requests.post(url, headers=headers, cookies=cookies, data=data)

print(response.text)
print(response)
