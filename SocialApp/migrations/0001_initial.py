# Generated by Django 2.2.16 on 2020-09-28 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Slide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.IntegerField(verbose_name='滑动用户')),
                ('sid', models.IntegerField(verbose_name='被滑动的用户')),
                ('slide_type', models.CharField(choices=[('like', '喜欢'), ('superlike', '超级喜欢'), ('dislike', '不喜欢')], max_length=10, verbose_name='滑动类型')),
                ('slide_time', models.DateTimeField(auto_now_add=True, verbose_name='滑动时间')),
            ],
            options={
                'db_table': 'slide',
                'unique_together': {('uid', 'sid')},
            },
        ),
        migrations.CreateModel(
            name='Friend',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid1', models.IntegerField(verbose_name='uid1')),
                ('uid2', models.IntegerField(verbose_name='uid2')),
            ],
            options={
                'db_table': 'friend',
                'unique_together': {('uid1', 'uid2')},
            },
        ),
    ]
