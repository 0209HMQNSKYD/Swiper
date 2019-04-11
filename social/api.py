from django.shortcuts import render

from common import error
from lib.http import render_json
from social import logics
from user.models import User


def get_rcmd_user(request):

    uid = request.session.get('uid')

    user = User.objects.get(id=uid)

    users = logics.get_rcmd_users(user)

    users_list = [user.to_string() for user in users]

    return render_json(users_list)

def like(request):
    # 判断是否是post请求
    if not request.method == "POST":
        return render_json("request method error", error.REQUEST_ERROR)

    sid = int(request.POST.get("sid"))

    mathed = logics.like(request.user,sid)

    return render_json({"mathed":mathed})

def superlike(request):
    # 判断是否是post请求
    if not request.method == "POST":
        return render_json("request method error", error.REQUEST_ERROR)

    sid = int(request.POST.get("sid"))

    mathed = logics.superlike(request.user, sid)

    return render_json({"mathed": mathed})

def dislike(request):
    # 判断是否是post请求
    if not request.method == "POST":
        return render_json("request method error", error.REQUEST_ERROR)

    sid = int(request.POST.get("sid"))

    logics.dislike(request.user,sid=sid)

    return render_json(None)

def regret(request):
    breaked = logics.regret(request.user)

    render_json({"regret":breaked})

def get_friends(request):
    pass


def get_friend_info(request):
    pass


