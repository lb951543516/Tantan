from django.core.cache import cache
from django.http import JsonResponse

from UserApp.logics import send_code
from UserApp.models import User, Profile
from UserApp.forms import UserForm, ProfileForm

# 用户获取手机验证码
from libs.qn_cloud import get_token, get_res_url


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
            # 添加 用户资料
            profile = Profile.objects.create(id=user.id)
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
    profile = Profile.objects.filter(id=uid)[0]

    data = {
        'code': 0,
        'data': profile.to_dict(),
    }
    return JsonResponse(data=data)


# 更新个人资料
def update_profile(request):
    # 定义form对象
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    # 检查验证数据
    if user_form.is_valid() and profile_form.is_valid():
        uid = request.session.get('uid')

        # 更新用户个人信息
        User.objects.filter(id=uid).update(**user_form.cleaned_data)
        Profile.objects.filter(id=uid).update(**profile_form.cleaned_data)

        print(user_form.cleaned_data)
        print(profile_form.cleaned_data)

        data = {
            'code': 0,
            'data': '修改信息成功'
        }
        return JsonResponse(data=data)
    else:
        err = {}
        err.update(user_form.errors)
        err.update(profile_form.errors)
        data = {
            'code': 1003,
            'data': err,
        }
        return JsonResponse(data=data)


# 获取七牛云 Token
def qn_token(request):
    uid = request.session.get('uid')
    filename = f'Avatar-{uid}'
    token = get_token(uid, filename)

    data = {
        'code': 0,
        'data': {
            'key': filename,
            'token': token,
        },
    }
    return JsonResponse(data=data)


# 七牛云回调
def qn_callback(request):
    uid = int(request.POST.get('uid'))
    # 获取上传⾄云服务后的⽂件名
    key = request.POST.get('key')

    avatar_url = get_res_url(key)
    User.objects.filter(id=uid).update(avatar=avatar_url)

    data = {
        'code': 0,
        'data': avatar_url,
    }
    return JsonResponse(data=data)
