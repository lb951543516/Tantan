import json
import time
import requests
from hashlib import md5

from Tantan import config


# 发送手机验证码
def send_sms(phonenum, code):
    args = {
        'appid': config.SD_APPID,  # 你的appid
        'to': phonenum,  # 收件人手机号
        'project': config.SD_PROJECT,  # 短信模版id
        'vars': json.dumps({'code': code}),  # jsonstring类型
        'timestamp': int(time.time()),  # 时间撮 整数
        'sign_type': config.SD_SIGN_TYPE,  # md5 or sha1 or normal
    }

    # 安装关键字进行排序升序排列
    sorted_args = sorted(args.items(), key=lambda d: d[0])
    # 创建签名字符串：以"key=value" + "&"（连接符）+ "key=value"的方式连接所有参数
    args_str = '&'.join([f'{k}={v}' for k, v in sorted_args])
    # 在创建的字符串前后加上APPID和APPKEY拼接签名字符串,
    sign_str = f'{config.SD_APPID}{config.SD_APPKEY}{args_str}{config.SD_APPID}{config.SD_APPKEY}'.encode('utf8')
    # 然后使用md5(string)或sha1(string)创建签名
    signature = md5(sign_str).hexdigest()

    args['signature'] = signature

    response = requests.post(config.SD_API, data=args)
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            return True
    return False
