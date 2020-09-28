from SocialApp.models import Slide, Friend
from UserApp.models import User
from VipApp.logics import perm_required
from libs.http import render_json
from SocialApp import logics
from common import errors


# 推荐用户
def rcmd_users(request):
    users = logics.rcmd(request.uid)
    data = [user.to_dict() for user in users]
    return render_json(data=data, code=errors.OK)


# 我的喜欢
def like(request):
    sid = int(request.POST.get('sid'))
    is_matched = logics.like_someone(request.uid, sid)

    data = {'is_matched': is_matched}
    return render_json(data=data)


# 超级喜欢
@perm_required('superlike')
def super_like(request):
    sid = int(request.POST.get('sid'))
    is_matched = logics.superlike_someone(request.uid, sid)

    data = {'is_matched': is_matched}
    return render_json(data=data)


# 不喜欢
def dislike(request):
    sid = int(request.POST.get('sid'))
    logics.dislike_someone(request.uid, sid)
    return render_json()


# 反悔
@perm_required('rewind')
def rewind(request):
    logics.rewind_slide(request.uid)
    return render_json()


# 喜欢我的
@perm_required('fans')
def fans(request):
    # 我滑过的人的id
    my_slide_list = Slide.objects.filter(uid=request.uid).values_list('sid', flat=True)

    # 查看除了我滑过的以外，喜欢我的人
    slides_list = Slide.objects.filter(
        sid=request.uid, slide_type__in=['like', 'superlike']
    ).exclude(uid__in=my_slide_list).values_list('uid', flat=True)

    user_list = User.objects.filter(id__in=slides_list)
    data = [user.to_dict() for user in user_list]
    return render_json(data=data)


# 好友列表
def friends(request):
    fid_list = Friend.find_friends(request.uid)
    user_list = User.objects.filter(id__in=fid_list)

    data = [user.to_dict() for user in user_list]
    return render_json(data=data)
