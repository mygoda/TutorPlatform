# coding=utf-8

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from . import serializers as student_serializers
from . import models as student_models
# Create your views here.


class StudentViewset(viewsets.ModelViewSet):
    """学员接口"""

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
            return Response({'status': False, 'msg': '%s 已存在' % student_phone})
        # 新增student
        student_id = student_models.Student.add_student(**params)
        return Response({'status': True, 'student_id': student_id})

    def destroy(self, request, pk=None):
        """
            删除学生
        :param request:
        :param pk: 学生id
        :return:
        """
        print('start delete teacher %s' % pk)
        student = student_models.Student.objects.get(id=pk)
        student.delete_student()
        return Response({'status': True, 'student_id': pk})
