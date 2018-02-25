# coding=utf-8
from django.http import JsonResponse


def created_json_response(data={}):
    """
        添加资源成功返回
    :param data:
    :return:
    """
    return JsonResponse(status=201, data=data)


def success_json_response(data={}):
    """
        成功返回
    :param data:
    :return:
    """
    return JsonResponse(status=200, data={"status": "ok", "data": data})


def error_json_response(data={}):
    """
        错误返回
    :param data:
    :return:
    """
    data["status"] = "error"
    return JsonResponse(data=data)