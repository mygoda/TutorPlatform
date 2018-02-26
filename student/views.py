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