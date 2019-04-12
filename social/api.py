from django.shortcuts import render

from common import error
from lib.http import render_json
from social import logics
from user.models import User
from vip.logics import check_permission


def get_rcmd_user(request):

    uid = request.session.get('uid')

    user = User.objects.get(id=uid)

    users = logics.get_rcmd_users(user)

    users_list = [user.to_string() for user in users]

    return render_json(users_list)


def like(request):
    # 判断是否是post请求
    if not request.method == "POST":
        return render_json("request method error", error.REQUEST_ERROR.code)

    sid = int(request.POST.get("sid"))

    mathed = logics.like(request.user,sid)

    return render_json({"mathed":mathed})


@check_permission("superlike")
def superlike(request):
    # 判断是否是post请求
    if not request.method == "POST":
        return render_json("request method error", error.REQUEST_ERROR.code)

    sid = int(request.POST.get("sid"))

    mathed = logics.superlike(request.user, sid)

    return render_json({"mathed": mathed})


def dislike(request):
    # 判断是否是post请求
    if not request.method == "POST":
        return render_json("request method error", error.REQUEST_ERROR.code)

    sid = int(request.POST.get("sid"))

    logics.dislike(request.user,sid=sid)

    return render_json(None)


@check_permission("rewind")
def regret(request):
    logics.regret(request.user)
    return render_json(" regret OK")


def get_friends(request):
    friends = request.user.friends
    flist = [friend.to_string() for friend in friends]
    return  render_json(flist)


def get_friend_info(request):
    # 判断是否是post请求
    if not request.method == "POST":
        return render_json("request method error", error.REQUEST_ERROR.code)

    fid = int(request.POST.get("fid"))

    user = logics.get_friend_info(request.user,fid)

    return render_json(user.to_string())

@check_permission("show_liked_me")
def get_who_liked_me(request):
    users = logics.get_who_liked_me(request.user)
    userlist = [user.to_string() for user in users]
    return render_json(userlist)