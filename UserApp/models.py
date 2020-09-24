from django.db import models


class User(models.Model):
    '''用户个人模型'''
    GENDERS = (
        ('male', '男性'),
        ('female', '女性'),
    )
    LOCATIONS = (
        ('北京', '北京'),
        ('上海', '上海'),
        ('深圳', '深圳'),
        ('成都', '成都'),
        ('沈阳', '沈阳'),
        ('西安', '西安'),
        ('武汉', '武汉'),
    )

    nickname = models.CharField(max_length=20, db_index=True, verbose_name='昵称')
    phonenum = models.CharField(max_length=16, unique=True, verbose_name='手机号')
    gender = models.CharField(max_length=10, choices=GENDERS, default='male', verbose_name='性别')
    birthday = models.DateField(default='2000-01-01', verbose_name='生日')
    avatar = models.CharField(max_length=256, verbose_name='头像')
    location = models.CharField(max_length=10, choices=LOCATIONS, default='上海', verbose_name='所在地')

    class Meta:
        db_table = 'user'

    @property
    def profile(self):
        _profile, _ = Profile.objects.get_or_create(user_id=self.id)
        return _profile

    def to_dict(self):
        return {
            'id': self.id,
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'gender': self.gender,
            'birthday': str(self.birthday),
            'avatar': self.avatar,
            'location': self.location,
        }


class Profile(models.Model):
    '''用户匹配对象的模型'''

    dating_gender = models.CharField(max_length=10, choices=User.GENDERS, default='female', verbose_name='匹配性别')
    dating_location = models.CharField(max_length=10, choices=User.LOCATIONS, default='上海', verbose_name='目标城市')
    max_distance = models.FloatField(default=10, verbose_name='最大查找范围')
    min_distance = models.FloatField(default=0, verbose_name='最小查找范围')
    max_dating_age = models.IntegerField(default=60, verbose_name='最大交友年龄')
    min_dating_age = models.IntegerField(default=15, verbose_name='最小交友年龄')
    vibration = models.BooleanField(default=False, verbose_name='开启震动')
    only_matched = models.BooleanField(default=False, verbose_name='允许查看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    class Meta:
        db_table = 'profile'

    def to_dict(self):
        return {
            'dating_gender': self.dating_gender,
            'dating_location': self.dating_location,
            'max_distance': self.max_distance,
            'min_distance': self.min_distance,
            'max_dating_age': self.max_dating_age,
            'min_dating_age': self.min_dating_age,
            'vibration': self.vibration,
            'only_matched': self.only_matched,
            'auto_play': self.auto_play,
        }
