import json
import time
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
import base64
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def generate_signed_request(query_dict: dict, private_key_pem: str) -> dict:
    # 生成唯一消息ID和时间戳
    msg_id = f"fp123"
    send_time = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

    # 构造body部分
    body = {
        "version": "1.0.0",
        "trnsType": "financial-products",
        "trnsId": msg_id,
        "exts": query_dict
    }

    body_str = json.dumps(body, sort_keys=True, separators=(',', ':'))
    key = RSA.import_key(private_key_pem)
    digest = SHA256.new(body_str.encode('utf-8'))
    signature = pkcs1_15.new(key).sign(digest)
    b64_signature = base64.b64encode(signature).decode('utf-8')

    # 构造header部分
    header = {
        "sendSysname": "fis",
        "msgType": "financial-products",
        "msgId": msg_id,
        "sendTime": send_time,
        "exts": {
            "signature": b64_signature
        }
    }

    # 组合完整请求
    return {
        "header": header,
        "body": body
    }


def aes_encrypt(plain_bytes: bytes, aes_key: bytes, aes_iv: bytes) -> bytes:
    return AES.new(aes_key, AES.MODE_CBC, aes_iv).encrypt(pad(plain_bytes, AES.block_size))


def encrypt_request_body(plain_text: str) -> str:
    aes_key = bytes.fromhex("6257384a633633557a3749314e355239")
    aes_iv = bytes.fromhex("30303030303030303030303030303030")
    return base64.b64encode(aes_encrypt(plain_text.encode(), aes_key, aes_iv)).decode()


if __name__ == '__main__':
    # 示例私钥（实际使用时替换为真实私钥）
    private_key = """-----BEGIN PRIVATE KEY-----
    MIIEvwIBADANBgkqhkiG9w0BAQEFAASCBKkwggSlAgEAAoIBAQCVjCcveuLIfM8dLjYE/6mYDmjqX0zrzyu+exAjXnhwVdQclSfY2Yv2tutUVcEo73vZZfoso/hAvuDhL7rsatwu4noQ4i/Eb2OIyfcXofkVxakYkfrQagzUdu1xFPxTPHtD3U7HGyZ6XVVZVnat+MlkGN5Dm2AGXKbFj1vip4EzKxHPA6eDM3dRzJj1kuiFA7bxf84qunKQ+cOpECZbWYiSF6sYf0n3evlkkrAWmtlyo5HBpYRWQUhZPH57k60c8p+CmM3LB4SoaMNBg5Q8OzQPovN+AELDnRRwDIEMUE7Mxw/4QWZI1PRhpeBoM/3MgvEY/mFi/cj1ht8UttuCAIzJAgMBAAECggEBAIBwqisWUPa+cyfty4mJh0BIiAVbqnYRLdHgYiDuf2SD4rRVyq5tUc+olP+O02J0JRu3gSGcBpidGAlv9AwfT1KZQxuDGGGPBZ6zT5wliggQBsZKgm9D1hcYuZ/Y1Uor9PZ5ebJ5+Bc6WBZts2qB9X4Z+bN5HAT6yGV/VfyZvtaRQ6LFiFKV48YToo9bi8PCrzonmVBJ5NXj522aTrLB0RIpfxR8A+DCZa0rd/pTd3zWdjHBqr6ffjWIRP+Ur/aeO/KtVZaaEXNDeFQwqKgXsBJfFRvHeorV6HH6Pg7nsBxwMlbmGcz2lhf62a7rlmVRnyRadGAzGtUkfK15RHHKo+0CgYEAzgz9eHnQ7VnoNQHnr9BoCAcVKQY+DzPwnrDvICPaPKVwKUMA5zJsx08Sas6qaO1h6ukIkUekhT17PS+nUKHsg/Np7w6SNaEAyceu0TJw+gLOuFfNXgnvUpxloDOY/a+8xZtt9P+OpxJIYPPQgoc7qWWbdYu6NsjRpg8ha1qxCzcCgYEAucy0+Nq4YhAzMoXc9GMFnRL7Z7GCLDtqzgLulrzPNAmthxwgJICh3dYq9yZZbd4arJk41qhE/R6b480zUYuldktxLjEtndCCvfceQprjFNwghzLuTUMs6YTLH0J9AV27Mx8L/Zvr2UacP/NGfYk32cuoMeSAV8MTjTLWeNcXJ/8CgYEAykpciuvlXzCWVXwiTyxnBgKWFqmnQdu3TsTcbwxj1IiDXi8G8vRBcUdDCJMPIGZ1bGAOZjsU3S6oEED5naLrBfxysxz2FCqWEIO3MHC6E+mvs7GX0MwmJk+fQjGF8QGYbdSTliVTktjTMEQOICfOPhegET31upVbphFSuQfXqu8CgYEAjBrEIJ91yGSk5qUwr4x38DEfKNse6NHJQR3O4hXwPTJLCwX3au8goBJehc4CQ6nm/V3xEVUD6McLEGVtHEGsfJ548zccSdOwsyTESb9YGyO+15RdRB+yn0iGjsTpVH1kqzDvLsdDuqzXKBX/gqxVVEORSkYfTY6JkMDUH306NesCgYBETMw2qRlHUsJ1065aOD5c0U2K5ZOO0XBud+oPz0gTiWXh0Qls89lqTzC2PVdOXoku5VqhbxNCIbk59rHM/U4HafU/mdAiqe0vBTOJfdbQ0vFwDtHR3z1aAA/JgTpLShNLeqW2XpCV4Cqi5blDjLsxdy6v9IkoduEHimtV2NQYtA==
    -----END PRIVATE KEY-----"""

    # 查询参数
    query_params = {
        "orgName": "",
        "prodName": "",
        "prodRegCode": "",
        "pageNum": 1,
        "pageSize": 20,
        "prodStatus": "",
        "prodSpclAttr": "",
        "prodInvestNature": "",
        "prodOperateMode": "",
        "prodRiskLevel": "",
        "prodTermCode": "",
        "actDaysStart": None,
        "actDaysEnd": None
    }

    # 生成带签名的请求
    signed_request = generate_signed_request(query_params, private_key)
    # 转换为JSON字符串
    json_request = json.dumps(signed_request, separators=(",", ":"))
    print(json_request)

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

    response = requests.post(
        'https://xinxipilu.chinawealth.com.cn/platformApi/lcxp-platService/product/getProductList',
        cookies=cookies,
        headers=headers,
        data=encrypt_request_body(json_request),
    )
    print(response.text)
    print(response)
