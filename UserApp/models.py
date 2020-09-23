from django.db import models


class User(models.Model):
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
    gender = models.CharField(max_length=10, choices=GENDERS, verbose_name='性别')
    birthday = models.DateField(default='2000-01-01', verbose_name='生日')
    avater = models.CharField(max_length=256, verbose_name='头像')
    location = models.CharField(max_length=10, choices=LOCATIONS, verbose_name='所在地')

    class Meta:
        db_table = 'user'
