from django.shortcuts import render

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
    pass


def superlike(request):
    pass


def dislike(request):
    pass


def regret(request):
    pass


def get_friends(request):
    pass


def get_friend_info(request):
    pass


