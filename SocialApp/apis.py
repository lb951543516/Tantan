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
    return render_json()


# 不喜欢
def dislike(request):
    return render_json()


# 反悔
def rewind(request):
    return render_json()


# 喜欢我的
def fans(request):
    return render_json()


# 好友列表
def friends(request):
    return render_json()


# 我的热度排名
def rank(request):
    return render_json()
