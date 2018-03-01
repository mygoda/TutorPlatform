# coding=utf-8
"""
    家教老师 api
"""

import logging

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from . import serializers as teacher_serializers
from . import models as teacher_models

logger = logging.getLogger(__name__)

# Create your views here.


class TeacherViewset(viewsets.ModelViewSet):
    """教师接口"""

    serializer_class = teacher_serializers.TeacherSerializer

    def get_queryset(self):
        return teacher_models.Teacher.objects.filter(is_valid=True)

    def get_serializer_class(self):
        """
            获取序列化
        :return:
        """
        if self.action == 'create':
            return teacher_serializers.TeacherSerializer
        else:
            return teacher_serializers.TeacherSerializer

    def create(self, request, *args, **kwargs):
        """
            创建教师
        :param request:
        :param args:
        :param kwargs:
        :param customer: {

                }
        :param phone:
        :param phone:
        :param phone:
        :param phone:
        :param phone:
        :param phone:
        :param phone:

        :return:
        """
        # 序列化参数
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        teacher_id = params.get('uid')
        logger.info('start create teacher %s info %s' % (teacher_id, params))

        return Response({'status': 'success'})


