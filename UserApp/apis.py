from django.core.cache import cache
from django.http import JsonResponse

from UserApp.logics import send_code
from UserApp.models import User, User_setting


# 用户获取手机验证码
def fetch_code(request):
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
def submit_code(request):
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
            user = User.objects.filter(phonenum=phonenum)[0]

            data = {
                'code': 0,
                'data': user.to_dict(),
            }
            return JsonResponse(data=data)

        # 如果验证码正确 没有帐号时...
        elif user_num == 0:
            # 添加 用户
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)
            # 添加 用户设置
            user_setting = User_setting.objects.create(user_id=user.id)
            # 设置session
            request.session['uid'] = user.id

            data = {
                'code': 0,
                'data': user.to_dict(),
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
    uid = request.session.get('uid')
    user_setting_info = User_setting.objects.filter(user_id=uid)[0]

    data = {
        'code': 0,
        'data': user_setting_info.to_dict(),
    }
    return JsonResponse(data=data)


# 更新个人资料
def update_profile(request):
    uid = request.session.get('uid')
    user = User.objects.get(pk=uid)
    user_set = User_setting.objects.filter(user_id=uid)[0]

    # 获取用户提交来的数据
    nickname = request.POST.get('nickname', user.nickname)
    birthday = request.POST.get('birthday', user.birthday)
    gender = request.POST.get('gender', user.gender)
    location = request.POST.get('location', user.location)

    dating_gender = request.POST.get('dating_gender', user_set.dating_gender)
    dating_location = request.POST.get('dating_location', user_set.dating_location)
    max_distance = request.POST.get('max_distance', user_set.max_distance)
    min_distance = request.POST.get('min_distance', user_set.min_distance)
    max_dating_age = request.POST.get('max_dating_age', user_set.max_dating_age)
    min_dating_age = request.POST.get('min_dating_age', user_set.min_dating_age)
    vibration = request.POST.get('vibration', user_set.vibration)
    only_matched = request.POST.get('only_matched', user_set.only_matched)
    auto_play = request.POST.get('auto_play', user_set.auto_play)

    # 更新用户个人信息
    user.nickname = nickname
    user.birthday = birthday
    user.gender = gender
    user.location = location
    user.save()

    user_set.dating_gender = dating_gender
    user_set.dating_location = dating_location
    user_set.max_distance = max_distance
    user_set.min_distance = min_distance
    user_set.max_dating_age = max_dating_age
    user_set.min_dating_age = min_dating_age
    user_set.vibration = vibration
    user_set.only_matched = only_matched
    user_set.auto_play = auto_play
    user_set.save()

    data = {
        'code': 0,
        'data': '修改信息成功'
    }
    return JsonResponse(data=data)


# 获取七牛云 Token
def qn_token(request):
    return None


# 七牛云回调接口
def qn_callback(request):
    return None
