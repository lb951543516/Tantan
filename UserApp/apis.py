from django.core.cache import cache
from django.http import JsonResponse

from UserApp.logics import send_code
from UserApp.models import User


# 用户获取手机验证码
def fetch_vcode(request):
    phonenum = request.GET.get('phonenum')

    if send_code(phonenum):
        data = {
            'code': 0,
            'data': None,
        }
        return JsonResponse(data=data)
    else:
        data = {
            'code': 1000,
            'data': '验证码发送失败',
        }
        return JsonResponse(data=data)


# 提交手机验证码
def submit_vcode(request):
    phonenum = request.POST.get('phonenum')
    code = request.POST.get('code')

    # 检查验证码是否正确
    key = 'code-%s' % phonenum
    cache_code = cache.get(key)

    # 验证码正确时...
    if code and code == cache_code:
        user_num = User.objects.filter(phonenum=phonenum).count()
        # 如果验证码正确并且已有帐号时...
        if user_num == 1:
            user_info = User.objects.filter(phonenum=phonenum)[0]
            data = {
                'code': 0,
                'data': {
                    'id': user_info.id,
                    'nickname': user_info.nickName,
                    'phonenum': user_info.userPhone,
                    'birthday': user_info.birthday,
                    'gender': user_info.gender,
                    'location': user_info.location,
                },
            }
            return JsonResponse(data=data)

        # 如果验证码正确 没有帐号时...
        elif user_num == 0:
            # 添加用户
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)
            # 设置session
            request.session['uid'] = user.id

            data = {
                'code': 0,
                'data': {
                    'id': user.id,
                    'nickname': user.nickname,
                    'phonenum': user.phonenum,
                    'birthday': user.birthday,
                    'gender': user.gender,
                    'location': user.location,
                },
            }
            return JsonResponse(data=data)
    # 验证码错误时...
    else:
        data = {
            'code': 1001,
            'data': '验证码错误',
        }
        return JsonResponse(data=data)


# 查看个人资料
def show_profile(request):
    return None
