# coding=utf-8

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models
from common import serializers as common_serializer


# get student serializer

class StudentTypeSerializer(serializers.ModelSerializer):
    """ 学生的不足"""

    student_type = common_serializer.StudentTypeSerializer()

    class Meta:
        model = models.StudentTypesShip
        fields = ("id", "student_type")


class StudentTeacherTypeSerializer(serializers.ModelSerializer):
    """学生对教室要求 教师特点"""

    teacher_type = common_serializer.TeacherTypeSerializer()

    class Meta:
        model = models.StudentTeacherTypes
        fields = ("id", "teacher_type")


class StudentSerializer(serializers.ModelSerializer):

    city = common_serializer.CitySerializer()
    subject = common_serializer.SubjectSerializer()
    level = common_serializer.LevelSerializer()
    student_types = StudentTypeSerializer(many=True)
    teacher_types = StudentTeacherTypeSerializer(many=True)
    follower_count = serializers.IntegerField()

    class Meta:
        model = models.Student
        fields = "__all__"


# create student serializer

class CreateStudentTypeSerializer(serializers.ModelSerializer):
    """创建 学生的不足"""

    class Meta:
        model = models.StudentTypesShip
        fields = ("id", "student_type")


class CreateStudentTeacherTypeSerializer(serializers.ModelSerializer):
    """创建 学生对教师要求 教师特点"""

    class Meta:
        model = models.StudentTeacherTypes
        fields = ("id", "teacher_type")


class CreateStudentSerializer(serializers.ModelSerializer):
    """
        创建学生
    """
    student_types = serializers.ListField(required=True)
    teacher_types = serializers.ListField(required=True)
    class Meta:
        model = models.Student
        fields = "__all__"


# 学生被收藏序列化

class CreateStudentFollowerSerializer(serializers.ModelSerializer):
    """
        收藏学生
    """

    class Meta:
        model = models.StudentFollowers
        fields = '__all__'
