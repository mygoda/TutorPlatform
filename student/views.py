# -*- coding: utf-8 -*-

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
            return student_serializers.UpdateStudentSerializer
        else:
            return student_serializers.StudentSerializer

    def create(self, request, *args, **kwargs):
        """
            添加学生    
        :param request:    
        :param args:    
        :param kwargs:{    
                "customer": "1",            用户id    
                "name": "小学生",            家长姓氏    
                "city": "1",                城市id    
                "level": "1",               年级id    
                "phone": "15201170495",     电话    
                "times": 1,                 学习次数，1：一周一次， 2：一周2次，依次内推，最大7次, 0: 面议    
                "basis": "1",               学习基础id    
                "sex": 0,                   性别，0：女 1：男    
                "money": 100,               薪水    
                "require": "211高校",        教师资质    
                "teacher_sex": 1,           教师性别    
                "subject": 6,               科目id    
                "address": "上课地点都行",   上课地点    
                "teacher_types": [    
                    {'teacher_type': 1},    
                    {'teacher_type': 2}    
                ],                          教师特点id list    
                "student_types": [    
                    {'student_type': 1},    
                    {'student_type': 2}      
                ],                          学生不足id        
                "extra": "其他"              其他        
            }            
             
        :return:{           
                status: 0/1         返回状态  目前0失败，1成功              
                student_id: 1       新增的学生id             
            }             
        """    
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        # print('start create student info %s' % params)
        # 新增student
        status, msg = student_models.Student.add_student(**params)
        if status:
            print('add student %s success' % msg)
            return Response({'status': 1, 'student_id': msg})
        # print('add student %s error msg %s' % (params, msg))
        return Response({'status': 0, 'msg': msg})

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
        return Response({'status': 1, 'student_id': pk})

    def update(self, request, pk=None):
        """
            修改学生
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        update_student = student_models.Student.objects.get(id=pk)
        update_student.update_student(**params)
        return Response({'status': 1, 'student_id': pk})

    def list(self, request, *args, **kwargs):
        """
            获取学生list              
            支持分页，默认每页20条                  
            当has_next 为 false 时，表示没有下一页了         
        :param request:       
        :param args:        
        :param kwargs:       
        :return:         
        """
        queryset = self.get_queryset()
        # 实现filter
        data = request.GET
        if int(data.get('city', 0)):
            queryset = queryset.filter(city_id=data.get('city'))
        if int(data.get('baselevel', 0)):
            queryset = queryset.filter(level__base_id=data.get('baselevel'))
        if int(data.get('subject', 0)):
            queryset = queryset.filter(subject_id=data.get('subject'))

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
              "student": 1,             被收藏学生id          
              "customer": 1             操作的用户id          
            }              
        :return:{          
            'status': 0/1,              返回状态  目前0失败，1成功          
            'student_follower_id': 1    收藏id,           
            'msg': '收藏失败'            失败时信息         
        }            
        """

        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        print('start add student followers info %s' % params)
        student_follower_id = student_models.StudentFollowers.add_student_follower(**params)
        if student_follower_id:
            return Response({'status': 1, 'student_follower_id': student_follower_id})
        print("add student follower error, is already exists. params: %s" % params)
        return Response({'status': 0, 'msg': '收藏失败'})

    def destroy(self, request, pk=None):
        """
            删除 学生 的收藏
        :param request:
        :param pk: 收藏id
        :return:
        """
        print('start delete student follower %s' % pk)
        student_follower = student_models.StudentFollowers.objects.get(id=pk)
        student_follower.delete_student_follower()
        print('delete student follower %s success' % pk)
        return Response({'status': 1, 'teacher_id': pk})

