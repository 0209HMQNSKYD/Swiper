import datetime

from common import keys
from lib.http import render_json
from user.models import User
from social.models import Swipe, Friend
from django.core.cache import cache
from swiper.config import REGRET_TIMES
from common import error

def get_rcmd_users(user):
    '''
    :param user:
    :return:推荐的用户列表
    '''
    current_year = datetime.date.today().year

    #推荐用户的出生最大年份：eg 2001
    max_dating_year = current_year - user.profile.min_dating_age
    #推荐用户的出生最小年份：eg 1973
    min_dating_year = current_year - user.profile.max_dating_age

    #已经滑动过的用户id
    swiped = Swipe.objects.filter(uid=user.id).only('sid')

    swiped_uid_list = [swipe.sid for swipe in swiped]
    # 排除自己
    swiped_uid_list.append(user.id)

    users = User.objects.filter(
        sex=user.profile.dating_sex,
        location=user.profile.location,
        birth_year__range=[min_dating_year,max_dating_year],
    ).exclude(id__in=swiped_uid_list)[0:20]

    #用户列表
    return users

def like(user,sid):

    #创建一条喜欢的滑动记录
    Swipe.swipe("like",uid=user.id,sid=sid)

    #查看对方是否喜欢过该用户user
    if Swipe.is_someone_like_you(uid=sid,sid=user.id):
        Friend.make_friend(user.id,sid)
        '''to_do:消息推送到对方手机，你们匹配成功'''
        return True

    else:
        return False

def superlike(user,sid):

    #创建一条喜欢的滑动记录
    Swipe.swipe("superlike",uid=user.id,sid=sid)

    #查看对方是否喜欢过该用户user
    if Swipe.is_someone_like_you(uid=sid,sid=user.id):
        Friend.make_friend(user.id,sid)
        '''to_do:消息推送到对方手机，你们匹配成功'''
        return True

    else:
        return False


def dislike(user,sid):
    # 创建一条不喜欢的滑动记录
    Swipe.swipe("dislike", uid=user.id, sid=sid)

def regret(user):
    #当前年与日
    now = datetime.date.today()
    #  格式化之后变为xxxx-xx-xx
    key = keys.REGRET_KEY%(user.id,now)
    #0,读不到则令为0,默认值
    regret_times = cache.get(key,0)

    #当前时间（具体到分秒）
    now_time = datetime.datetime.now()

    if regret_times < REGRET_TIMES:
        #now_second为一天剩余的秒：一天的秒数-当前的秒数
        now_second = now_time.hour*3600+now_time.minute*60+now_time.second
        cache.set(key,86400-now_second)
        try:
        #反悔操作，删除好友关系
            #获取最后一次该用户滑动的记录，
            record = Swipe.objects.filter(uid=user.id).latest("stime")

        #查询你们现在是否是好友，如果是则解除好友

            #删除好友关系
            Friend.break_up(uid1=user.id,uid2=record.sid)
            #删除滑动记录
            record.delete()
        except Swipe.DoesNotExist:
            raise error.MODEL_ERROR("model error")

    else:
        raise error.REACH_REGRET_LIMIT("reach regret limit")

def get_friend_info(user,fid):
    friends = user.friends
    flist = [friend.to_string() for friend in friends]

    if fid not in flist:
        raise error.NO_THIS_USER("no this friend")
    users = User.objects.filter(id=fid)

    if not users:
        raise error.NO_THIS_USER("no this user")

    user = users.first()
    return user


def get_who_liked_me(user):
    liked_user_ids = Swipe.who_liked_me(user.id)
    users = User.objects.filter(id__in=liked_user_ids)
    return users