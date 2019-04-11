
from django.http import HttpResponse
from django.shortcuts import render
from common import error
from django.core.cache import  cache
from common import keys
from lib.sms import send_sms
from lib.http import render_json
from  user.models import *
from user.forms import ProfileForm
from user.logics import upload_avatar_to_server


def submit_phone(request):
    """获取短信验证码"""
    if not request.method == "POST":
        return render_json("request method error",code=error.REQUEST_ERROR)

    phone = request.POST.get("phone")

    result,msg = send_sms(phone)
    # data = {"dage"}

    return render_json(msg)

def submit_vcode(request):
    """通过验证码登录注册"""
    #判断是否是post请求
    if not request.method=="POST":
        return render_json("request method error",error.REQUEST_ERROR)

    phone = request.POST.get("phone")
    # 获取手机收到的验证码
    vcode = request.POST.get("vcode")
    print("++++++++",vcode)
    # 获取缓存中的验证码
    cache_vcode = cache.get(keys.VCODE_KEY%phone)
    #对比两个验证码是否相等
    if vcode == cache_vcode:
        #有则获取，无则创建用户
        user,_ = User.objects.get_or_create(phonenum=phone,nickname=phone)
        request.session["uid"] = user.id

        return  render_json(user.to_string())
    else:
        return render_json("verify code error",error.VCODE_ERROR)

def get_profile(request):
    """获取个人资料"""
    uid = request.session.get("uid")
    print(uid)
    if uid != None:
        user = User.objects.get(id=uid)

        #获取个人资料，没有则自动创建
        profile = user.profile

        return render_json(profile.to_string())



def set_profile(request):
    """修改个人资料"""
    if not request.method == "POST":
        return render_json("request method error",error.REQUEST_ERROR)

    uid = request.session.get("uid")

    #request.POST实际是一个字典
    profile_form = ProfileForm(request.POST)

    #判断表单数据是否通过验证
    if profile_form.is_valid():
        profile = profile_form.save(commit=False)
        profile.id = uid
        profile.save()
        return render_json("modify profile success")
    else:
        return render_json(profile_form.errors,error.FORM_VALID_ERROR)



def upload_avtar(request):
    """头像上传"""
    if not request.method == "POST":
        return render_json("request method error",error.REQUEST_ERROR)

    #获取上传的头像
    avatar = request.FILES.get("avatar")
    #获取该头像的用户id
    uid = request.session.get("uid")
    #把头像保存到本地路径
    upload_avatar_to_server(uid,avatar)

    return render_json("uppoad success")
