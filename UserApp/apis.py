import logging
from UserApp.logics import send_vcode
from UserApp.models import User, Profile
from UserApp.forms import UserForm, ProfileForm
from common import errors, keys
from libs.qn_cloud import get_token, get_res_url
from libs.cache import rds
from libs.http import render_json

inf_log = logging.getLogger('inf')

from libs.qn_cloud import get_token, get_res_url
from libs.cache import rds
from libs.http import render_json


# 用户获取手机验证码
def fetch_code(request):
    phonenum = request.GET.get('phonenum')
    # 异步调用--异步发送短信验证码
    send_vcode.delay(phonenum)

    return render_json()


# 提交手机验证码
def submit_code(request):
    phonenum = request.POST.get('phonenum')
    vcode = request.POST.get('vcode')

    # 检查验证码是否正确
    key = keys.VCODE_K % phonenum
    cache_code = rds.get(key)

    # 验证码正确时...
    if vcode and vcode == cache_code:
        user_num = User.objects.filter(phonenum=phonenum).count()
        # 如果验证码正确并且已有帐号时...
        if user_num == 1:
            user = User.objects.filter(phonenum=phonenum)[0]
            inf_log.info(f'User Login:{user.id}/{user.phonenum}')

            request.session['uid'] = user.id

            return render_json(data=user.to_dict())

        # 如果验证码正确 没有帐号时...
        elif user_num == 0:
            # 添加 用户
            user = User.objects.create(phonenum=phonenum, nickname=phonenum)
            # 添加 用户资料
            profile = Profile.objects.create(id=user.id)
            # 日志
            inf_log.info(f'User Register:{user.id}/{user.phonenum}')
            # 设置session
            request.session['uid'] = user.id

            return render_json(data=user.to_dict())
    # 验证码错误时...
    else:
        raise errors.VcodeErr('验证码错误')


# 查看个人资料
def show_profile(request):
    uid = request.session.get('uid')
    key = keys.PROFILE_K % uid

    # 先从缓存获取数据，没有就冲数据库获取，然后存在缓存里面
    profile = rds.get(key)
    inf_log.debug(f'从缓存中获取数据: {profile}')

    if profile is None:
        profile, _ = Profile.objects.get_or_create(id=uid)
        inf_log.debug(f'从数据库中获取数据: {profile}')
        rds.set(key, profile)
        inf_log.debug('将数据写入到缓存')


    return render_json(data=profile.to_dict())


# 修改个人资料
def update_profile(request):
    # 定义form对象，，注意两个模型的字段不能同名
    user_form = UserForm(request.POST)
    profile_form = ProfileForm(request.POST)

    # 检查验证数据
    if user_form.is_valid() and profile_form.is_valid():
        uid = request.uid

        # 更新用户个人信息-------- **字典名，可以按照相同的key进行传值
        User.objects.filter(id=uid).update(**user_form.cleaned_data)
        Profile.objects.filter(id=uid).update(**profile_form.cleaned_data)

        inf_log.debug('删除旧缓存')
        rds.delete(keys.PROFILE_K % uid)

        return render_json(data='修改信息成功')
    else:
        err = {}
        err.update(user_form.errors)
        err.update(profile_form.errors)
        raise errors.ProfileErr(data=err)


# 获取七牛云 Token
def qn_token(request):
    uid = request.session.get('uid')
    filename = f'Avatar-{uid}'
    token = get_token(uid, filename)

    data = {
        'key': filename,
        'token': token,
    }
    return render_json(code=errors.OK, data=data)


# 七牛云回调
def qn_callback(request):
    uid = int(request.POST.get('uid'))
    # 获取上传⾄云服务后的⽂件名
    key = request.POST.get('key')

    avatar_url = get_res_url(key)
    User.objects.filter(id=uid).update(avatar=avatar_url)

    return render_json(data=avatar_url, code=errors.OK)
