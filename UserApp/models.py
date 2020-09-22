from django.db import models


class User(models.Model):
    nickName = models.CharField(max_length=16, null=True, blank=True)
    userPhone = models.CharField(max_length=20)
    gender = models.NullBooleanField(default=None)
    birthday = models.DateTimeField(default='2000-01-01')
    location = models.CharField(max_length=16, default='保密')

    class Meta:
        db_table = 'user'
