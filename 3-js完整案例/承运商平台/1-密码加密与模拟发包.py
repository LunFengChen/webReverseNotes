import hashlib
import requests


def calc_pwd(username: str, password: str) -> str:
    original_string = username.lower() + password
    r = original_string.encode()
    for _ in range(1024):
        r = hashlib.sha1(r).digest()
    return r.hex()


headers = {
    "Accept": "application/json",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "Connection": "keep-alive",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Origin": "https://carrier.okguanli.com",
    "Referer": "https://carrier.okguanli.com/",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\""
}
cookies = {
    "JSESSIONID": "58C866308DB153BDDF3890C3E2A3505F",
    "SESSION": "NzMxNTJlNDAtOTg3Yy00OTk5LWEyNjYtYTM5NmJmYTZkMDE5"
}
url = "https://carrier.okguanli.com/api/login"
username = "1"
password = "kkk"
data = {
    "username": username,
    "password": calc_pwd(username, password),
    "bpType": "CARRIER",
    "corp": "LANXIN",
    "authenticationProvider": "CARRIER"
}
response = requests.post(url, headers=headers, cookies=cookies, data=data)

print(response.text)
print(response)
