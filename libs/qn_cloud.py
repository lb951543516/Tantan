import json
import time
from qiniu import Auth

from Tantan import config


def get_token(uid, filename):
    img_url = f'http://{config.QN_DOMAIN}/{filename}'
    policy = {
        'scope': config.QN_BUCKET,
        'deadline': int(time.time() + 600),  # 有效时间10分钟
        'returnBody': json.dumps({'code': 0, 'data': img_url}),
        'callbackUrl': config.QN_CALLBACK_URL,  # 回调访问服务器的地址
        'callbackHost': config.QN_CALLBACK_DOMAIN,  # 云服务器地址/ip
        'callbackBody': f'key={filename}&uid={uid}',  # 上传成功后 七牛云想服务器发送的东西
        'forceSaveKey': True,  # 自定义文件名字
        'saveKey': filename,
        'fsizeLimit': 10485760,  # 文件最大是10M
        'mimeLimit': 'image/*',  # 只允许上传图片
    }

    qn_auth = Auth(config.QN_ACCESS_KEY, config.QN_SECRET_KEY)

    token = qn_auth.upload_token(config.QN_BUCKET, filename, 600, policy)
    return token


# 返回图片地址
def get_res_url(filename):
    return f'http://{config.QN_DOMAIN}/{filename}'
