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
        elif self.action == "list":
            return teacher_serializers.TeacherSerializer
        elif self.action == "update":
            return teacher_serializers.CreateTeacherSerializer
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
                {"subject": 1},    
                {}    
            ],    
            teacher_types: [
                {'teacher_type': 1},
                {}
            ],
            self_introduction: 自我介绍
        }
                  
        :return:{    
                status: 返回状态  True/Fasle    
                teacher_id: 教师id    
            }    
        """    
        # 序列化参数    
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        print('start create teacher info %s' % params)
        status, msg = teacher_models.Teacher.add_teacher(**params)
        if status:
            print('add teacher %s success' % msg)
            return Response({'status': 1, 'teacher_id': msg})
        print('add teacher %s error msg %s' % (params, msg))
        return Response({'status': 0, 'msg': msg})

    def update(self, request, pk=None):
        """
            修改教师
        :param request:
        :param pk:
        :return:
        """
        pass

    def destroy(self, request, pk=None):
        """
            删除老师
        :param request:
        :param pk: 教师id
        :return:
        """
        print('start delete teacher %s' % pk)
        teacher = teacher_models.Teacher.objects.get(id=pk)
        teacher.delete_teacher()
        print('delete teacher %s success' % pk)
        return Response({'status': 1, 'teacher_id': pk})

    def list(self, request, *args, **kwargs):
        """
            获取教师list
            支持分页
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 获取 教师 queryset
        queryset = self.get_queryset()
        # 获取分页信息
        page = self.paginate_queryset(queryset=queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # 没有分页时
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class TeacherFollowerViewset(viewsets.ModelViewSet):
    """
        教师收藏api
    """

    def get_queryset(self):
        return teacher_models.TeacherFollowers.objects.filter(is_valid=True)

    def get_serializer_class(self):
        """
            获取序列化
        :return:
        """
        if self.action == 'create':
            return teacher_serializers.CreateTeacherFollowerSerializer
        else:
            return teacher_serializers.CreateTeacherFollowerSerializer

    def create(self, request, *args, **kwargs):
        """
            点击收藏  教师
        :param request:
        :param args:
        :param kwargs:{
              "teacher": "1",
              "follower_id": "1"
            }
        :return: {
            'status': 0,
            'teacher_follower_id': 收藏id,
            'msg': '失败时信息'
        }
        """

        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        print('start add teacher followers info %s' % params)
        teacher_follower_id = teacher_models.TeacherFollowers.add_teacher_follower(**params)
        if teacher_follower_id:
            return Response({'status': True, 'teacher_follower_id': teacher_follower_id})
        print("add teacher follower error, is already exists. params: %s" % params)
        return Response({'status': 0, 'msg': '收藏失败'})

