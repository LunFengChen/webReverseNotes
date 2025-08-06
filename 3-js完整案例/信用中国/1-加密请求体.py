import uuid
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
from gmssl import sm2, func


def sm4_ecb_encrypt(plaintext: bytes, key: bytes) -> bytes:
    crypt_sm4 = CryptSM4()
    crypt_sm4.set_key(key, SM4_ENCRYPT)
    return crypt_sm4.crypt_ecb(plaintext)


def encrypt_queryContent(params_dct: dict) -> str:
    params_str = "&".join([f"{k}={v}" for k, v in params_dct.items()])
    cipher_bytes = sm4_ecb_encrypt(params_str.encode(), bytes.fromhex("dbb78b8b64d640bb130255c69e959973"))
    return cipher_bytes.hex()


def generate_nonceStr() -> str:
    return str(uuid.uuid4()).replace("-", "")


def sm2_signer(data: str) -> str:
    # 16进制的公钥和私钥
    private_key = '3945208F7B2144B13F36E38AC6D39F95889393692860B51A42FB81EF4DF7C5B8'
    public_key = '04F4C1ECFDF9B6DDFF6B1B3A2A0B8A7D5A2B8E0D4F1A3E7C7F8B1A9F0D3C6B2E5C7D8F0A3B1C5D6E7F8A9B0C1D2E3F4A5B6C7D8E9F0A1B2'
    appId = "27IGtFrNFDc"

    sm2_crypt = sm2.CryptSM2(public_key=public_key, private_key=private_key)

    random_hex_str = func.random_hex(sm2_crypt.para_len)
    sign = sm2_crypt.sign(data.encode(), random_hex_str)  # 16进制
    return sign


if __name__ == '__main__':
    data = "appId=27IGtFrNFDc&encryptType=SM4&nonceStr=239378bf4ea5409c860ac38443d6a40f&queryContent=12622f46d0f9fcc905f33dee85faffe131244ee277cc8ef5d7df2e4ad5afd7b9&signType=SM2&timestamp=1753869338832&version=1.0"
    res = sm2_signer(data)
    print(res)
