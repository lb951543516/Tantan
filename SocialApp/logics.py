import datetime

from SocialApp.models import Slide, Friend
from UserApp.models import User
from UserApp.models import Profile
from common import keys
from libs.cache import rds


def rcmd(uid):
    '''推荐用户'''
    profile = Profile.objects.get(id=uid)

    # 计算出生日期范围
    today = datetime.date.today()
    earliest_birth = today - datetime.timedelta(days=profile.max_dating_age * 365)
    latest_birth = today - datetime.timedelta(days=profile.min_dating_age * 365)

    # 仅仅获取已经划过的人的sid
    sid_list = Slide.objects.filter(uid=uid).values_list('sid', flat=True)

    users = User.objects.filter(
        location=profile.dating_location,
        gender=profile.dating_gender,
        birthday__range=[earliest_birth, latest_birth]
    ).exclude(id__in=sid_list)[:20]

    return users


def like_someone(uid, sid):
    '''喜欢的人'''
    # 1.添加滑动记录
    Slide.objects.create(uid=uid, sid=sid, slide_type='like')

    # 2.检查对方是否喜欢自己，如果喜欢那么建立好友关系
    is_like = Slide.is_liked(uid=sid, sid=uid)
    if is_like is True:
        Friend.make_friend(uid, sid)
        return True
    else:
        return False


def superlike_someone(uid, sid):
    '''超级喜欢'''
    # 1.添加滑动记录
    Slide.objects.create(uid=uid, sid=sid, slide_type='superlike')

    # 2.检查对方是否喜欢自己，如果喜欢那么建立好友关系
    is_like = Slide.is_liked(uid=sid, sid=uid)
    if is_like is True:
        Friend.make_friend(uid, sid)
        return True
    elif is_like is False:
        return False
    else:
        # 对方没有滑到自己，将自己添加到对方的优先推荐队列
        rds.lpush(keys.FIRST_RCMD_Q % sid, uid)
