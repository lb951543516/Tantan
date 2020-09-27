from django.db import models


class Slide(models.Model):
    '''滑动记录表'''
    STYPES = (
        ('like', '喜欢'),
        ('superlike', '超级喜欢'),
        ('dislkie', '不喜欢'),
    )
    uid = models.IntegerField(verbose_name='滑动用户')
    sid = models.IntegerField(verbose_name='被滑动的用户')
    slide_type = models.CharField(max_length=10, choices=STYPES, verbose_name='滑动类型')
    slide_time = models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')

    class Meta:
        # 设置联合唯一，不能对同一个用户进行两次操作
        unique_together = ['uid', 'sid']
        db_table = 'slide'


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
