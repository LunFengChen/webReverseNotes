import random
import time

import execjs


def calc_sign(sign_str: str) -> str:
    with open('1-扣sign算法.js', 'r') as f:
        js_code = f.read()
    ctx = execjs.compile(js_code)
    result = ctx.call('calc_sign', sign_str)
    return result


if __name__ == '__main__':
    nonceStr = "".join(random.sample("0123456789", 8))
    timestamp = int(time.time() * 1000)
    sign_str = f"appSignKey=4bTogwpz7RzNO2VTFtW7zcfRkAE97ox6ZSgcQi7FgYdqrHqKB7aGqEZ4o7yssa2aEXoV3bQwh12FFgVNlpyYk2Yjm9d2EZGeGu3&noncestr={nonceStr}&timestamp={timestamp}"
    sign = calc_sign(sign_str)
    print(sign)
