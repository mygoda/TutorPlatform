# coding=utf-8

from django.http import JsonResponse
from django.shortcuts import render

from libs import uuid
from libs import upload

# Create your views here.


def upload_file(request):
    """
        上传文件
    :param request:
    :return:
    """
    # user_info = UserInfo.objects.get(user_id=request.user.id)
    files = request.FILES
    up_file = files.get("file")
    size = up_file.size / 1000
    stream = up_file.read()
    file_name = up_file.name
    key = "%s%s" % (uuid.create_uuid(), up_file.name)
    result = upload.upload_stream_to_qiniu(key=key, data=stream)
    # user_info.add_user_point(type=PointType.UPLOAD)
    return JsonResponse({'url': result, "key": key, "size": size, "name": file_name})

