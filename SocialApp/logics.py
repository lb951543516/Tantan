import datetime
from django.db.transaction import atomic

from SocialApp.models import Slide, Friend
from UserApp.models import User
from UserApp.models import Profile
from common import keys
from common import errors
from libs.cache import rds
from Tantan import config


def rcmd_from_queue(uid):
    '''从推荐列表进行推荐'''
    # 结果是2进制列表,取20个
    uid_list = rds.lrange(keys.FIRST_RCMD_Q % uid, 0, 19)
    # 转换成int类型
    uid_list = [int(uid) for uid in uid_list]

    users = User.objects.filter(id__in=uid_list)
    return users


def rcmd_from_db(uid, num=20):
    '''从数据库中推荐用户'''
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
    ).exclude(id__in=sid_list)[:num]

    return users


def rcmd(uid):
    '''推荐用户'''
    first_users = rcmd_from_queue(uid)
    remain = 20 - len(first_users)
    if remain > 0:
        second_users = rcmd_from_db(uid, num=remain)
        return set(first_users) | set(second_users)
    else:
        return first_users


# 将函数放在事务中执行，出错会自动回滚，成功自动提交

@atomic
def like_someone(uid, sid):
    '''喜欢的人'''
    # 1.添加滑动记录
    Slide.slide(uid=uid, sid=sid, slide_type='like')

    # 2.强制删除优先推荐队列里的id
    rds.lrem(keys.FIRST_RCMD_Q % uid, count=0, value=sid)

    # 给被滑动者添加积分
    rds.zincrby(keys.HOT_RANK, config.SLIDE_SCORE['like'], sid)

    # 3.检查对方是否喜欢自己，如果喜欢那么建立好友关系
    is_like = Slide.is_liked(uid=sid, sid=uid)
    if is_like is True:
        Friend.make_friend(uid, sid)
        return True
    else:
        return False


@atomic
def superlike_someone(uid, sid):
    '''超级喜欢'''
    # 1.添加滑动记录
    Slide.slide(uid=uid, sid=sid, slide_type='superlike')

    # 2.强制删除优先推荐队列里的id
    rds.lrem(keys.FIRST_RCMD_Q % uid, count=0, value=sid)


    # 给被滑动者添加积分
    rds.zincrby(keys.HOT_RANK, config.SLIDE_SCORE['superlike'], sid)

    # 3.检查对方是否喜欢自己，如果喜欢那么建立好友关系
    is_like = Slide.is_liked(uid=sid, sid=uid)
    if is_like is True:
        Friend.make_friend(uid, sid)
        return True
    elif is_like is False:
        return False
    else:
        # 对方没有滑到自己，将自己添加到对方的优先推荐队列
        rds.lpush(keys.FIRST_RCMD_Q % sid, uid)
        return False


def dislike_someone(uid, sid):
    '''不喜欢'''
    # 1.添加滑动记录
    Slide.slide(uid=uid, sid=sid, slide_type='dislike')

    # 2.强制删除优先推荐队列里的id
    rds.lrem(keys.FIRST_RCMD_Q % uid, count=0, value=sid)

    # 给被滑动者添加积分
    rds.zincrby(keys.HOT_RANK, config.SLIDE_SCORE['dislike'], sid)


def rewind_slide(uid):
    '''反悔(每天3次，5分钟内)'''
    now_time = datetime.datetime.now()
    today = now_time.date()
    rewind_key = keys.REWIND_K % (today, uid)

    # 检查是否已经3次
    rewind_num = rds.get(rewind_key, 0)
    if rewind_num >= config.REWIND_TIMES:
        raise errors.RewindLimit

    # 检查最后一次滑动是否在5分钟内
    last_slide = Slide.objects.filter(uid=uid).latest('slide_time')

    if now_time > last_slide.slide_time + datetime.timedelta(minutes=config.REWIND_TIMEOUT):
        raise errors.RewindTimeout

    # 将多次数据修改在事务中执行
    with atomic():

        # 检查是否是好友
        if last_slide.slide_type in ['like', 'superlike']:
            Friend.broken(uid, last_slide.sid)

            if last_slide.slide_type == 'superlike':
                # 从对方的推荐列表里删除我的id
                rds.lrem(keys.FIRST_RCMD_Q % last_slide.sid, count=0, value=uid)


        # 撤回被滑动者的积分
        score = config.SLIDE_SCORE[last_slide.slide_type]
        rds.zincrby(keys.HOT_RANK, -score, last_slide.sid)

        # 删除最后一次滑动
        last_slide.delete()

        # 设置缓存，反悔次数加一
        rds.set(rewind_key, rewind_num + 1, 86400)


def get_top_n(RANK_NUM):
    '''获取排行榜前n名的用户数据'''
    # 从redis里取出原始数据
    origin_data = rds.zrevrange(keys.HOT_RANK, 0, RANK_NUM - 1, withscores=True)
    # 原始数据转换成int类型
    cleaned_data = [[int(uid), int(score)] for uid, score in origin_data]

    # 用户的id列表
    uid_list = [item[0] for item in cleaned_data]

    # 数据库取数据
    users = User.objects.filter(id__in=uid_list)
    users = sorted(users, key=lambda user: uid_list.index(user.id))

    # 整理数据
    rank_data = []
    for index, (uid, score) in enumerate(cleaned_data):
        rank = index + 1
        user = users[index]
        user_data = user.to_dict(exclude=['phonenum', 'birthday', 'location',
                                          'vip_id', 'vip_end'])
        user_data['rank'] = rank
        user_data['score'] = score
        rank_data.append(user_data)

    return rank_data
