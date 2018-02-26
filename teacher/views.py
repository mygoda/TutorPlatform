# coding=utf-8

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from . import serializers as teacher_serializers
from . import models as teacher_models
# Create your views here.


class TeacherViewset(viewsets.ModelViewSet):
    """学员接口"""

    serializer_class = teacher_serializers.TeacherSerializer

    def get_queryset(self):
        return teacher_models.Teacher.objects.filter(is_valid=True)