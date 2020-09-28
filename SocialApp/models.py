from django.db import models
from django.db import IntegrityError
from django.db.models import Q

from common import errors


class Slide(models.Model):
    '''滑动记录表'''
    STYPES = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislike', '不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动用户')
    sid = models.IntegerField(verbose_name='被滑动的用户')
    slide_type = models.CharField(max_length=10, choices=STYPES, verbose_name='滑动类型')
    slide_time = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:
        # 设置联合唯一，不能对同一个用户进行两次操作
        unique_together = ['uid', 'sid']
        db_table = 'slide'

    @classmethod
    def slide(cls, uid, sid, slide_type):
        try:
            cls.objects.create(uid=uid, sid=sid, slide_type=slide_type)
        except IntegrityError:
            # 抛出重复滑动异常
            raise errors.RepeatSlideErr

    @classmethod
    def is_liked(cls, uid, sid):
        slide = Slide.objects.filter(uid=uid, sid=sid).first()
        if not slide:
            return None
        elif slide.slide_type in ['like', 'superlike']:
            return True
        elif slide.slide_type == 'dislike':
            return False


class Friend(models.Model):
    '''好友表'''
    uid1 = models.IntegerField(verbose_name='uid1')
    uid2 = models.IntegerField(verbose_name='uid2')

    class Meta:
        unique_together = ['uid1', 'uid2']
        db_table = 'friend'

    @classmethod
    def make_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        cls.objects.create(uid1=uid1, uid2=uid2)

    @classmethod
    def broken(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        cls.objects.filter(uid1=uid1, uid2=uid2).delete()

    @classmethod
    def find_friends(cls, uid):
        condition = Q(uid1=uid) | Q(uid2=uid)
        friend_list = Friend.objects.filter(condition)

        fid_list = []
        for f in friend_list:
            if f.uid1 == uid:
                fid_list.append(f.uid2)
            else:
                fid_list.append(f.uid1)

        return fid_list
