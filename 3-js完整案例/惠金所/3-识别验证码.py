import ddddocr
from loguru import logger


ocr = ddddocr.DdddOcr(show_ad=False)

with open("2-验证码图片.png", "rb") as f:
    img_binary = f.read()

code = ocr.classification(img_binary)
logger.success(f"验证码识别结果: {code}")

