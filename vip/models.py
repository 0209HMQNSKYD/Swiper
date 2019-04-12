from django.db import models

class Vip(models.Model):
    name = models.CharField(max_length=20,verbose_name="会员名称")
    level = models.IntegerField(verbose_name="等级")
    price = models.FloatField(verbose_name="价格")

    @property
    def perms(self):
        #查询跟自身vip对应的vip_perm_relation表，找到所有的perm_id
        vip_perm_relations = VipPermRelation.objects.filter(vip_id=self.id)

        #获取此vip的权限id的列表
        perm_id_list = [vip_perm.perm_id for vip_perm in vip_perm_relations]

        return Permission.objects.filter(id__in = perm_id_list)


    def has_perm(self,perm_name):
        '''查看是否有权限'''
        perms = self.perms
        for perm in perms:
            if perm.name == perm_name:
                return True

        return False


class Permission(models.Model):
    name = models.CharField(max_length=20)
    desc = models.TextField()


class VipPermRelation(models.Model):
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()
