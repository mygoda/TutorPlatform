# -*- coding: utf-8 -*-
"""
    家教老师 api
"""

import logging

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets

from common.exe import TokenException
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
            return teacher_serializers.UpdateTeacherSerializer
        else:
            return teacher_serializers.TeacherSerializer

    def create(self, request, *args, **kwargs):
        """
            创建教师    
        :param request:    
        :param args:    
        :param kwargs:{                    
            customer: 5             用户id          
            last_name: 谷           教师姓氏          
            city: 1                 城市id         
            school: 1               学校id         
            phone: '15201170495'    教师电话               
            sex: 1                  性别    /0：女 1：男           
            learn: 1                学历id             
            profession: 计算机       专业          
            high_score: 500         高考分数            
            money: 100              期望薪资 /默认单位：小时          
            head_image: ''          头像地址             
            subjects: [                 
                {"subject": 1},              
                {"subject": 2}                    
            ],                      擅长科目id list            
            teacher_types: [          
                {'teacher_type': 1},           
                {'teacher_type': 2}                   
            ],                      教师特点id list          
            self_introduction: 自我介绍          
        }          
                  
        :return:{           
                status: 0/1         返回状态  目前0失败，1成功          
                teacher_id: 1       新增的教师id           
            }         
        """        
        # 序列化参数    
        data = request.data
        customer = request.customer
        if not customer:
            raise TokenException('用户验证失败')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        params['customer'] = customer
        logger.info(u'start create teacher info %s' % params)

        # 添加教师
        status, msg = teacher_models.Teacher.add_teacher(**params)
        if status:
            print('add teacher %s success' % msg)
            return Response({'status': 1, 'teacher_id': msg})
        logger.info('add teacher %s error msg %s' % (params, msg))
        return Response({'status': 0, 'msg': msg})

    def update(self, request, pk=None):
        """
            修改教师         
        :param request:         
        :param pk:         
        :return:           
        """
        data = request.data
        # 验证用户
        if request.customer.teacher_set.filter(is_valid=True).first().id != int(pk):
            raise TokenException('用户验证失败')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        update_teacher = teacher_models.Teacher.objects.get(id=pk)
        update_teacher.update_teacher(**params)
        return Response({'status': 1, 'teacher_id': pk})

    def destroy(self, request, pk=None):
        """
            删除老师          
        :param request:       
        :param pk: 教师id         
        :return:            
        """
        print('start delete teacher %s' % pk)
        if request.customer.teacher_set.filter(is_valid=True).first().id != int(pk):
            raise TokenException('用户验证失败')
        teacher = teacher_models.Teacher.objects.get(id=pk)
        teacher.delete_teacher()
        print('delete teacher %s success' % pk)
        return Response({'status': 1, 'teacher_id': pk})

    def list(self, request, *args, **kwargs):
        """
            获取教师list            
            支持分页，默认每页20条                     
            当has_next 为 false 时，表示没有下一页了           
        :param request:          
        :param args:             
        :param kwargs:             
        :return:           
        """
        # 获取 教师 queryset
        queryset = self.get_queryset()
        # 实现filter
        data = request.GET
        if int(data.get('city', 0)):
            queryset = queryset.filter(city_id=data.get('city'))
        if int(data.get('school', 0)):
            queryset = queryset.filter(school_id=data.get('school'))
        if int(data.get('subject', 0)):
            queryset = queryset.filter(teachersubjectsship__subject__id=data.get('subject'))

        # 获取分页信息
        page = self.paginate_queryset(queryset=queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        # 没有分页时
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """

        :param request:
        :param pk:
        :return:
        """
        customer = request.customer
        if not customer:
            raise TokenException('用户验证失败')
        teacher = teacher_models.Teacher.objects.get(id=pk)
        serializer = teacher_serializers.TeacherSerializer(teacher)
        teacher_info = serializer.data
        teacher_info['customer_is_follower'] = teacher.customer_is_follower(customer_id=customer.id)
        return Response(teacher_info)


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
              "teacher": ",             被收藏教师id          
              "customer": 1             操作的用户id          
            }           
        :return: {              
            'status': 0/1,              返回状态  目前0失败，1成功            
            'teacher_follower_id': 1    收藏id,             
            'msg': '收藏失败'            失败时信息            
        }              
        """
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        customer = request.customer
        if not customer:
            raise TokenException('用户验证失败')
        params['customer'] = customer
        print('start add teacher followers info %s' % params)
        teacher_follower_id, msg = teacher_models.TeacherFollowers.add_teacher_follower(**params)
        if teacher_follower_id:
            return Response({'status': 1, 'teacher_follower_id': teacher_follower_id})
        print("add teacher follower error, is already exists. params: %s" % params)
        return Response({'status': 0, 'msg': msg})

    def destroy(self, request, pk=None):
        """
            删除 教师 的收藏
        :param request:
        :param pk: 收藏id
        :return:
        """
        print('start delete teacher follower %s' % pk)
        teacher_follower = teacher_models.TeacherFollowers.objects.get(id=pk)
        if request.customer != teacher_follower.customer:
            raise TokenException('用户验证失败')
        teacher_follower.delete_teacher_follower()
        print('delete teacher follower %s success' % pk)
        return Response({'status': 1, 'teacher_id': pk})


class TeacherApplyViewset(viewsets.ModelViewSet):
    """
        申请教师
    """

    def get_queryset(self):
        return teacher_models.TeacherApply.objects.filter(is_valid=True)

    def get_serializer_class(self):
        """
            获取序列化
        :return:
        """
        if self.action == 'create':
            return teacher_serializers.CreateTeacherApplySerializer
        else:
            return teacher_serializers.CreateTeacherApplySerializer

    def create(self, request, *args, **kwargs):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pass