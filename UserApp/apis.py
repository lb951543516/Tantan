from django.http import JsonResponse

from UserApp.logics import send_code
from UserApp.models import User


# 用户获取手机验证码
def fetch_vcode(request):
    userphone = request.GET.get('userphone')
    if send_code(userphone):
        data = {
            'code': 0,
            'data': None,
        }
        return JsonResponse(data=data)
    else:
        data = {
            'code': 1000,
            'data': None,
        }
        return JsonResponse(data=data)


# 提交手机验证码
def submit_vcode(request):
    userphone = request.POST.get('userphone')
    vcode = request.POST.get('code')

    if vcode == 'yzm':
        userphone_num = User.objects.filter(userPhone=userphone).count()
        user_info = User.objects.filter(userPhone=userphone)[0]

        # 如果验证码正确并且已有帐号，进行登录
        if userphone_num == 1:
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

        # 如果验证码正确并且没有帐号，添加用户 然后再登录
        elif userphone_num == 0:
            user = User(userPhone=userphone)
            user.save()

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
    # 验证码错误
    else:
        data = {
            'code': 1001,
            'data': None,
        }
        return JsonResponse(data=data)


# 查看个人资料
def show_profile(request):
    return None
