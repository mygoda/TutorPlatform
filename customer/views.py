# coding=utf-8
"""
    用户api
"""

import logging

from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets
from libs import uuid, upload
from . import models as customer_models
from . import serializers as customer_serializers
from teacher import serializers as teacher_serializers
from student import serializers as student_serializers

logger = logging.getLogger(__name__)
# Create your views here.


def login(req):
    code = req.GET.get("code")
    print(req.META)
    print("code %s" % code)
    customer = customer_models.Customer.objects.all()[0]
    token = customer_models.CustomerTokenShip.new_customer_token(customer_id=customer.id)
    print(token)
    try:
        return JsonResponse(data={"token": token})
    except Exception as e:
        import traceback
        raise Exception(traceback.format_exc())


class CustomerViewset(viewsets.ModelViewSet):
    """
        用户 api
    """

    def get_queryset(self):
        return customer_models.Customer.objects.all()

    def get_serializer_class(self):
        """
            获取序列化
        :return:
        """

        return customer_serializers.CustomerSerializer

    @list_route(methods=["POST"])
    def upload_file(self, request):
        files = request.FILES
        up_file = files.get("file")
        size = up_file.size / 1000
        stream = up_file.read()
        file_name = up_file.name
        key = "%s%s" % (uuid.create_uuid(), up_file.name)
        result = upload.upload_stream_to_qiniu(key=key, data=stream)
        return Response({'url': result, "key": key, "size": size, "name": file_name})

    def retrieve(self, request, pk=None):
        """

        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        customer = request.customer
        serializer = customer_serializers.CustomerSerializer(customer)
        return Response(serializer.data)

    @detail_route(methods=["GET"])
    def issue(self, request, pk=None):
        """

        :param request:
        :param pk:
        :return:
        """
        customer = request.customer
        if customer.customer_type == 1:
            teacher = customer.teacher_set.filter(is_valid=True).first()
            serializer = teacher_serializers.TeacherSerializer(teacher)
            teacher_data = serializer.data
            teacher_data['customer_type'] = '教师'
            teacher_data['customer_type_id'] = 1
            return Response(teacher_data)
        elif customer.customer_type == 2:
            student = customer.student_set.filter(is_valid=True).first()
            serializer = student_serializers.StudentSerializer(student)
            student_data = serializer.data
            student_data['customer_type'] = '学生'
            student_data['customer_type_id'] = 2
            return Response(student_data)
        else:
            user_data = {}
            user_data['customer_type'] = '未注册'
            user_data['customer_type_id'] = 0
            return Response(user_data)

