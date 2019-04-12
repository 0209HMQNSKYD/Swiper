from django.db import models
from django.db.models import Q


class Swipe(models.Model):

    FLAGS = (
        ('like', '喜欢'),
        ('superlike','超级喜欢'),
        ('dislike', '不喜欢'),
        ('blacklist', '拉黑')
    )

    flag = models.CharField(max_length=10,choices=FLAGS, verbose_name='滑动状态')
    uid = models.IntegerField()
    sid = models.IntegerField()
    stime = models.DateTimeField(auto_now_add=True)

    @classmethod
    def swipe(cls,flag,uid,sid):
        return cls.objects.get_or_create(flag=flag, uid=uid, sid=sid)

    @classmethod
    def is_someone_like_you(cls, uid,sid):
        return cls.objects.filter(flag__in=["like","superlike"], uid=uid, sid=sid).exists()


class Friend(models.Model):

    uid1 = models.IntegerField()
    uid2 = models.IntegerField()
    ftime = models.DateTimeField(auto_now_add=True)

    @classmethod
    def make_friend(cls,uid1,uid2):
        uid1,uid2 = (uid1,uid2) if uid1 > uid2 else (uid2,uid1)
        cls.objects.create(uid1=uid1,uid2=uid2)

    @classmethod
    def break_up(cls,uid1,uid2):
        uid1, uid2 = (uid1, uid2) if uid1 > uid2 else (uid2, uid1)
        #删除好友关系
        cls.objects.filter(uid1=uid1,uid2=uid2).delete()

    @classmethod
    def get_friends_list(cls,uid):
        friends = cls.objects.filter(Q(uid1=uid)|Q(uid2=uid))
        fid_list = []
        for friend in friends:
            if friend.uid1 == uid:
                fid_list.append(friend.uid2)
            else:
                fid_list.append(friend.uid1)
        return fid_list