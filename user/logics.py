#author:HMQ
# -*- coding: utf-8 -*-
import os

from social.models import Swipe
from  swiper.settings import MEDIA_ROOT,BASE_DIR
from lib.http import render_json


def upload_avatar_to_server(uid,avatar):
    #定义头像名称，
    file_name = "avatat_%s" % uid + os.path.splitext(avatar.name)[1]

    #保存的路径：D:\python_stage4\day03\code\Swiper\media\uploads
    save_path = os.path.join(BASE_DIR, MEDIA_ROOT, file_name)

    with open(save_path, "wb") as fp:
        # 分块写入
        for chunk in avatar.chunks():
            fp.write(chunk)

