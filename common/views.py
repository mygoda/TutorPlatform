# coding=utf-8

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

from . import models as common_models
from . import serializers as common_serializers
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
    return JsonResponse(data={'url': result, "key": key, "size": size, "name": file_name}, status=200)


class CityViewset(viewsets.ModelViewSet):
    """
        城市 api view
    """

    def get_queryset(self):
        return common_models.City.objects.all()

    def get_serializer_class(self):
        """
            获取城市序列化
        :return:
        """
        return common_serializers.CitySerializer


class SubjectViewset(viewsets.ModelViewSet):
    """
        科目 api view
    """

    def get_queryset(self):
        return common_models.Subject.objects.all()

    def get_serializer_class(self):
        """
            获取 科目 序列化
        :return:
        """
        return common_serializers.SubjectSerializer


class BaseLevelViewset(viewsets.ModelViewSet):
    """
        年级 api view
    """

    def get_queryset(self):
        return common_models.BaseLevel.objects.all()

    def get_serializer_class(self):
        """
            获取 年级 序列化
        :return:
        """
        return common_serializers.BaseLevelSerializer


class LevelViewset(viewsets.ModelViewSet):
    """
        小学还是初中 api view
    """

    def get_queryset(self):
        return common_models.Level.objects.all()

    def get_serializer_class(self):
        """
            获取 序列化
        :return:
        """
        return common_serializers.LevelSerializer


class SchoolViewset(viewsets.ModelViewSet):
    """
        学校 api view
    """

    def get_queryset(self):
        return common_models.School.objects.all()

    def get_serializer_class(self):
        """
            获取 学校 序列化
        :return:
        """
        return common_serializers.SchoolSerializer


class TeacherTypeViewset(viewsets.ModelViewSet):
    """
        教师特点 api view
    """

    def get_queryset(self):
        return common_models.TeacherType.objects.all()

    def get_serializer_class(self):
        """
            获取 学校 序列化
        :return:
        """
        return common_serializers.TeacherTypeSerializer


class StudentTypeViewset(viewsets.ModelViewSet):
    """
        学生不足 api view
    """

    def get_queryset(self):
        return common_models.StudentType.objects.all()

    def get_serializer_class(self):
        """
            获取 学校 序列化
        :return:
        """
        return common_serializers.StudentTypeSerializer


class BasisViewset(viewsets.ModelViewSet):
    """
        学生基础 api view
    """

    def get_queryset(self):
        return common_models.Basis.objects.all()

    def get_serializer_class(self):
        """
            获取 学生基础 序列化
        :return:
        """
        return common_serializers.BasisSerializer


class LearnViewset(viewsets.ModelViewSet):
    """
        学历 api view
    """

    def get_queryset(self):
        return common_models.Learn.objects.all()

    def get_serializer_class(self):
        """
            获取 学历 序列化
        :return:
        """
        return common_serializers.LearnSerializer


class TeacherRequireViewset(viewsets.ModelViewSet):
    """
        教师资质 api view
    """

    def get_queryset(self):
        return common_models.TeacherRequire.objects.all()

    def get_serializer_class(self):
        """
            获取 教师资质 序列化
        :return:
        """
        return common_serializers.TeacherRequireSerializer


