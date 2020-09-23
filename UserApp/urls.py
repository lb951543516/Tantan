from django.urls import path
from UserApp import apis

urlpatterns = [
    # 提交手机号
    path('vcode/fetch/', apis.getPhone, name='vcode/fetch'),

    # 提交验证码，进行登录
    path('vcode/submit/', apis.login, name='vcode/submit'),

    # 获取验证码
    path('vcode/', apis.phone_vcore, name='vcode'),

]
