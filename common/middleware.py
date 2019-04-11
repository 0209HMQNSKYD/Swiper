#author:HMQ
# -*- coding: utf-8 -*-

from django.utils.deprecation import MiddlewareMixin

from common import error
from user.models import User
from lib.http import render_json

#中间件，判断是否登陆
class AuthMiddleware(MiddlewareMixin):
    URL_WHITE_LIST = [
        '/user/api/submit_phone',
        '/user/api/submit_vcode'
    ]

    def process_request(self,request):

        if request.path in self.URL_WHITE_LIST:
            return

        uid = request.session.get("uid")
        if not uid:
            return render_json("user not login",error.USER_NOT_LOGIN)
        try:
            user = User.objects.get(id=uid)
            request.user = user
        except User.DoesNotExist:
            return render_json("no this user",error.NO_THIS_USER)