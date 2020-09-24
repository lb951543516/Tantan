import random
import re
from django.core.cache import cache

from libs.send_sms import send_sms


# 验证手机号
def is_phonenum(phone):
    if re.search(r'^1[3-9]\d{9}$', phone):
        return True
    else:
        return False


# 生成指定长度的验证码
def make_code(length=6):
    code = [str(random.randint(0, 9)) for i in range(length)]
    return ''.join(code)


# 发送验证码
def send_code(phone):
    if not is_phonenum(phone):
        return False

    key = 'code-%s' % phone
    # 检查缓存是否存在，防止在有效时间内频繁发送验证码
    if cache.get(key):
        return True

    # 手机号正确，发送验证码
    code = make_code(6)
    print(code)
    # 设置缓存，设置验证码的有效时间
    cache.set(key, code, 600)
    return send_sms(phone, code)
