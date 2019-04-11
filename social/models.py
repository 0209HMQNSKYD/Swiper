from django.db import models

class Swipe(models.Model):

    FLAGS = (
        ('like', '喜欢'),
        ('superlike','超级喜欢'),
        ('dislike', '不喜欢'),
        ('blacklist', '拉黑')
    )

    flag = models.CharField(max_length=8,choices=FLAGS, verbose_name='滑动状态')
    uid = models.IntegerField()
    sid = models.IntegerField()
    stime = models.DateTimeField(auto_now_add=True)

class Friend(models.Model):

    uid1 = models.IntegerField()
    uid2 = models.IntegerField()
    ftime = models.DateTimeField(auto_now_add=True)
