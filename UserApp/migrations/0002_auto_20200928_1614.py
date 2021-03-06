# Generated by Django 2.2.16 on 2020-09-28 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='vip_end',
            field=models.DateTimeField(default='9999-12-31', verbose_name='vip过期时间'),
        ),
        migrations.AddField(
            model_name='user',
            name='vip_id',
            field=models.IntegerField(default=1, verbose_name='vip的id'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='only_matched',
            field=models.BooleanField(default=False, verbose_name='允许查看我的相册'),
        ),
    ]
