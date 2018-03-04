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
            return teacher_serializers.CreateTeacherSerializer
        elif self.action == 'retrieve':
            return teacher_serializers.TeacherSerializer
        else:
            return teacher_serializers.TeacherSerializer

    def create(self, request, *args, **kwargs):
        """
            创建教师
        :param request:
        :param args:
        :param kwargs:{
            customer: 用户id
            last_name: 教师姓氏
            city: 城市id
            school: 学校id
            phone: 电话
            sex: 性别    /0：女 1：男
            learn: 学历
            profession: 专业
            high_score: 高考分数
            money: 期望薪资 /默认单位：小时
            head_image: 头像
            subjects: [
                {},
                {}
            ],
            self_introduction: 自我介绍
        }


        :return:
        """
        # 序列化参数
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        print('start create teacher info %s' % params)
        # 新增教师
        teacher_id = teacher_models.Teacher.add_teacher(**params)
        return Response({'status': 'success', 'teacher_id': teacher_id})

