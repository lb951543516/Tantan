import datetime

from SocialApp.models import Slide, Friend
from UserApp.models import User
from UserApp.models import Profile


def rcmd(uid):
    '''推荐用户'''
    profile = Profile.objects.get(id=uid)

    today = datetime.date.today()
    earlist_birth = today - datetime.timedelta(days=profile.max_dating_age * 365)
    latest_birth = today - datetime.timedelta(days=profile.min_dating_age * 365)

    users = User.objects.filter(location=profile.dating_location, gender=profile.dating_gender,
                                birthday__range=[earlist_birth, latest_birth])[:20]

    # TODO:排除已经划过的人

    return users


def like_someone(uid, sid):
    '''喜欢的人'''
    # 1.添加滑动记录
    Slide.objects.create(uid=uid, sid=sid, slide_type='like')

    # 2.检查对方是否喜欢自己，如果喜欢那么建立好友关系
    is_like = Slide.objects.filter(uid=sid, sid=uid, slide_type__in=['like', 'superlike']).count()
    if is_like == 1:
        Friend.make_friend(uid, sid)
        return True
    else:
        return False
