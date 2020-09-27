from django.db.models import Max

from SocialApp.models import Slide
from UserApp.models import User
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
def rewind(request):
    last_slide = Slide.objects.filter(uid=request.uid).aggregate(Max('slide_time'))
    last_slide.delete()
    return render_json()


# 喜欢我的
def fans(request):
    slides_list = Slide.objects.filter(
        sid=request.uid, slide_type__in=['like', 'superlike']
    ).values_list('uid', flat=True)

    user_list = User.objects.filter(id__in=slides_list)
    data = [user.to_dict() for user in user_list]
    return render_json(data=data)


# 好友列表
def friends(request):
    return render_json()


# 我的热度排名
def rank(request):
    return render_json()
