from django.db import models


class User(models.Model):
    nickname = models.CharField(max_length=16)
    phonenum = models.CharField(max_length=20)
    gender = models.NullBooleanField(default=None)
    birthday = models.DateTimeField(default='2000-01-01')
    location = models.CharField(max_length=16)

    class Meta:
        db_table = 'user'
