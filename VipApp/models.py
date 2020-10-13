from django.db import models


class Vip(models.Model):
    '''会员表'''
    name = models.CharField(max_length=20, unique=True, verbose_name='vip种类')
    level = models.IntegerField(verbose_name='会员等级')
    duration = models.IntegerField(verbose_name='会员时长')
    price = models.FloatField(verbose_name='会员价格')

    class Meta:
        db_table = 'vip'

    def has_perm(self, perm_name):
        perm = Permission.objects.get(name=perm_name)
        result = VipPermRelation.objects.filter(vip_level=self.level, perm_id=perm.id).exists()
        return result


class Permission(models.Model):
    '''权限表'''
    name = models.CharField(max_length=20, unique=True, verbose_name='权限名称')
    description = models.TextField(verbose_name='权限描述')

    class Meta:
        db_table = 'permission'


class VipPermRelation(models.Model):
    '''会员-权限关系表'''
    vip_level = models.IntegerField(verbose_name='会员等级')
    perm_id = models.IntegerField(verbose_name='权限id')

    class Meta:
        db_table = 'vip_perm_relation'
