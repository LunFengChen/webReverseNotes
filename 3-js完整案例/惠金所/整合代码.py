import base64
import hashlib

import requests
from loguru import  logger
import ddddocr
import json


def get_img_and_token()->tuple[str, str]:
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Referer": "https://www.hfax.com/login.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
        "apiVersion": "1.9",
        "ds": "home",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "acw_tc": "ac11000117544862956312680e44ebc3ef130354d12f6702bbdfa954cf3ab8",
        "forever": "1",
        "sajssdk_2015_cross_new_user": "1",
        "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%221987f884c66f65-084019eea34463-4c657b58-1024000-1987f884c672139%22%2C%22%24device_id%22%3A%221987f884c66f65-084019eea34463-4c657b58-1024000-1987f884c672139%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D",
        "SESSION": "bcc1dc5b-0b9e-4ea0-a0e8-3ae9e3e808f2"
    }
    url = "https://www.hfax.com/pc-api/common/imageCode/login"
    response = requests.get(
        url,
        headers=headers,
        # cookies=cookies
    )

    img_b64 = response.json()['data']['base64Str'].split("data:image/png;base64,")[-1]
    img_token = response.json()['data']['token']
    logger.success(f"验证码图片token: {img_token}, 图片b64: {img_b64}")
    return img_b64, img_token

def write_img(img_b64: str) -> str:
    img_binary = base64.b64decode(img_b64)
    img_filename = "2-验证码图片.png"
    with open(img_filename, "wb") as f:
        f.write(img_binary)
        logger.success(f"已保存验证码图片: {img_filename}")
    return img_filename

def ocr_img(filename: str) -> str:
    ocr = ddddocr.DdddOcr(show_ad=False)
    with open(filename, "rb") as f:
        img_binary = f.read()

    code = ocr.classification(img_binary)
    logger.success(f"验证码识别结果: {code}")
    return code

def login(username: str, password: str, img_code: str, img_token: str) -> requests.Response:
    headers = {
        "Accept": "*/*",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Connection": "keep-alive",
        "Content-Type": "application/json;charset=UTF-8",
        "Origin": "https://www.hfax.com",
        "Referer": "https://www.hfax.com/login.html",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0",
        "X-Requested-With": "XMLHttpRequest",
        "apiVersion": "1.9",
        "distinctid": "1987f884c66f65-084019eea34463-4c657b58-1024000-1987f884c672139",
        "ds": "home",
        "sec-ch-ua": "\"Not)A;Brand\";v=\"8\", \"Chromium\";v=\"138\", \"Microsoft Edge\";v=\"138\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    cookies = {
        "forever": "1",
        "sajssdk_2015_cross_new_user": "1",
        "sensorsdata2015jssdkcross": "%7B%22distinct_id%22%3A%221987f884c66f65-084019eea34463-4c657b58-1024000-1987f884c672139%22%2C%22%24device_id%22%3A%221987f884c66f65-084019eea34463-4c657b58-1024000-1987f884c672139%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22%22%2C%22%24latest_referrer_host%22%3A%22%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%7D%7D",
        "SESSION": "bcc1dc5b-0b9e-4ea0-a0e8-3ae9e3e808f2"
    }
    url = "https://www.hfax.com/pc-api/user/login"
    data = {
        "username": username,
        "password": hashlib.md5(f"{password}TuD00Iqz4ge7gzIe2rmjSAFFKtaIBmnr8S".encode("utf-8")).hexdigest(),
        "imgCode": img_code,
        "imgToken": img_token
    }
    data = json.dumps(data, separators=(',', ':'))
    response = requests.post(
        url,
        headers=headers,
        # cookies=cookies,
        data=data
    )
    logger.success(response.text)
    return response

if __name__ == '__main__':
    img_b64, img_token = get_img_and_token()
    filename = write_img(img_b64)
    img_code = ocr_img(filename)
    login("18888888888", "123456", img_code, img_token)

