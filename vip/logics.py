#author:HMQ
# -*- coding: utf-8 -*-
from common import error


#检查用户的权限，通过装饰器实现
def check_permission(perm_name):
    def deco(view_fun):
        def wraper(request,*args,**kwargs):
            #判断当前用户是否有权限
            if request.user.vip.has_perm(perm_name):

                return view_fun(request,*args,**kwargs)
            else:
                raise error.NO_PERMISSION_ERROR("no %s permission"%perm_name)
        return wraper
    return deco