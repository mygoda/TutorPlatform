# coding=utf-8

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from . import serializers as student_serializers
from . import models as student_models
# Create your views here.


class StudentViewset(viewsets.ModelViewSet):
    """
        学员接口
        follower_count 是 此学生 被收藏数
    """

    serializer_class = student_serializers.StudentSerializer

    def get_queryset(self):
        return student_models.Student.objects.filter(is_valid=True)

    def get_serializer_class(self):
        """
            获取序列化
        :return:
        """
        if self.action == 'create':
            return student_serializers.CreateStudentSerializer
        elif self.action == 'retrieve':
            return student_serializers.StudentSerializer
        elif self.action == "list":
            return student_serializers.StudentSerializer
        elif self.action == "update":
            return student_serializers.StudentSerializer
        else:
            return student_serializers.StudentSerializer

    def create(self, request, *args, **kwargs):
        """
            添加学生    
        :param request:    
        :param args:    
        :param kwargs:{    
                "customer": "1",    
                "name": "小学生",    
                "city": "1",    
                "level": "1",    
                "phone": "15201170495",    
                "times": 1,     
                "learn": "1",     
                "study": "学习主动性差",    
                "sex": 0,    
                "money": 100,    
                "require": "211高校",    
                "teacher_sex": 1,    
                "subject": 6,    
                "address": "上课地点都行",    
                "teacher_types": [
                    {'teacher_type': 1},
                    {}
                ],
                "student_types": [
                    {'student_type': 1},
                    {}
                ],
                "extra": "其他"
            }    
    
        :return:    
        """    
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        print('start create student info %s' % params)
        student_phone = params.get("phone")
        if student_models.Student.objects.filter(phone=student_phone, is_valid=True).exists():
            print('phone %s is already exists' % student_phone)
            return Response({'status': False, 'msg': '%s 已存在' % student_phone})
        # 新增student
        student_id = student_models.Student.add_student(**params)
        print('add student %s success' % student_id)
        return Response({'status': True, 'student_id': student_id})

    def destroy(self, request, pk=None):
        """
            删除学生
        :param request:
        :param pk: 学生id
        :return:
        """
        print('start delete student %s' % pk)
        student = student_models.Student.objects.get(id=pk)
        student.delete_student()
        print('delete student %s success' % pk)
        return Response({'status': True, 'student_id': pk})

    def list(self, request, *args, **kwargs):
        """
            获取学生list
            支持分页
        :param request:
        :param args:
        :param kwargs:
        :return:
        """

        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset=queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class StudentFollowerViewset(viewsets.ModelViewSet):
    """
        学生收藏api
    """

    def get_queryset(self):
        return student_models.StudentFollowers.objects.filter(is_valid=True)

    def get_serializer_class(self):
        """
            获取序列化
        :return:
        """
        if self.action == 'create':
            return student_serializers.CreateStudentFollowerSerializer
        else:
            return student_serializers.CreateStudentFollowerSerializer

    def create(self, request, *args, **kwargs):
        """
            点击收藏学生
        :param request:
        :param args:
        :param kwargs:{
              "student": "1",
              "follower_id": "1"
            }
        :return:
        """

        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        print('start add student followers info %s' % params)
        student_follower_id = student_models.StudentFollowers.add_student_follower(**params)
        if student_follower_id:
            return Response({'status': True, 'student_follower_id': student_follower_id})
        print("add student follower error, is already exists. params: %s" % params)
        return Response({'status': False, 'msg': '收藏失败'})



