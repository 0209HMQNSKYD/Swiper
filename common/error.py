#author:HMQ
# -*- coding: utf-8 -*-

# REQUEST_ERROR = 4000
# NO_THIS_USER = 4001
# VCODE_ERROR= 4002
# FORM_VALID_ERROR= 4003
# USER_NOT_LOGIN = 4004

class LogicError(Exception):
    name = None
    code = None

    def __init__(self,data):
        self.data = data

def gen_logicerror(name,code):
    #类名
    return type(name,(LogicError,),{"code":code})

REQUEST_ERROR = gen_logicerror("REQUEST_ERROR",4000)
NO_THIS_USER = gen_logicerror("NO_THIS_USER",4001)
VCODE_ERROR= gen_logicerror("VCODE_ERROR",4002)
FORM_VALID_ERROR= gen_logicerror("FORM_VALID_ERROR",4003)
USER_NOT_LOGIN = gen_logicerror("USER_NOT_LOGIN",4004)
REACH_REGRET_LIMIT = gen_logicerror("REACH_REGRET_LIMIT",4005)
MODEL_ERROR = gen_logicerror("MODEL_ERROR",4006)
NO_PERMISSION_ERROR = gen_logicerror("NO_PERMISSION_ERROR",4007)