import json, time, requests
from hashlib import md5
from django.http import HttpResponse

from UserApp.models import User


def login(request):
    userphone = request.POST.get('userphone')
    verify_code = request.POST.get('post')

    userphone_num = User.objects.filter(userPhone=userphone).count()
    if userphone_num == 1:
        return HttpResponse('登录成功')
    elif userphone_num == 0:
        # 注册完成后自动登录
        user = User(userPhone=userphone)
        user.save()
        return HttpResponse('注册成功，正在登录')


def phone_vcore(request):
    appid = '54745'
    appkey = '30250544f5d3d8815fdd2976acf6a9ce'
    api = 'https://api.mysubmail.com/message/xsend.json'

    args = {
        'appid': '54745',  # 你的appid
        'to': '13029868285',  # 收件人手机号
        'project': 'irWcU4',  # 短信模版id
        'vars': json.dumps({'code': '123456'}),  # jsonstring类型
        'timestamp': int(time.time()),  # 时间撮 整数
        'sign_type': 'md5',  # md5 or sha1 or normal
    }

    # 安装关键字进行排序升序排列
    sorted_args = sorted(args.items(), key=lambda d: d[0])
    # 创建签名字符串：以"key=value" + "&"（连接符）+ "key=value"的方式连接所有参数
    args_str = '&'.join([f'{k}={v}' for k, v in sorted_args])
    # 在创建的字符串前后加上APPID和APPKEY拼接签名字符串,
    sign_str = f'{appid}{appkey}{args_str}{appid}{appkey}'.encode('utf8')
    # 然后使用md5(string)或sha1(string)创建签名
    signature = md5(sign_str).hexdigest()

    args['signature'] = signature

    response = requests.post(api, data=args)
    print(response.status_code)

    result = response.json()
    print(result)
    return HttpResponse('发送成功')
