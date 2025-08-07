import requests
import random
import time

import execjs


def calc_sign(sign_str: str) -> str:
    with open("1-扣sign算法.js", "r") as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    result = ctx.call("calc_sign", sign_str)
    return result


headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "origin": "https://search.dxy.cn",
    "priority": "u=1, i",
    "referer": "https://search.dxy.cn/",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
}
cookies = {
    "JUTE_SESSION_ID": "954809b5-854a-490a-8e3c-749c369b1c9b",
    "_clck": "5yq6yi%7C2%7Cfy8%7C0%7C2044",
    "_clsk": "1ldc85j%7C1754492430530%7C2%7C1%7Ck.clarity.ms%2Fcollect",
}
url = "https://bbsapi.dxy.cn/pc/loginInfo"
nonceStr = "".join(random.sample("0123456789", 8))
timestamp = int(time.time() * 1000)
sign_str = f"appSignKey=4bTogwpz7RzNO2VTFtW7zcfRkAE97ox6ZSgcQi7FgYdqrHqKB7aGqEZ4o7yssa2aEXoV3bQwh12FFgVNlpyYk2Yjm9d2EZGeGu3&noncestr={nonceStr}&timestamp={timestamp}"

params = {"timestamp": timestamp, "noncestr": nonceStr, "sign": calc_sign(sign_str)}
response = requests.get(
    url,
    headers=headers,
    # cookies=cookies,
    params=params,
)

print(response.text)
print(response)
