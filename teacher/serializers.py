# coding=utf-8

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models
from common import serializers as common_serializer


# get teacher serializer

class TeacherSubjectSerializer(serializers.ModelSerializer):
    """教师学科"""

    subject_name = serializers.CharField()

    class Meta:
        model = models.TeacherSubjectsShip
        fields = ("id", "subject_name", "subject_id")


class TeacherTypeSerializer(serializers.ModelSerializer):
    """教师特点"""

    teacher_type_name = serializers.CharField()

    class Meta:
        model = models.TeacherTypesShip
        fields = ("id", "teacher_type_name", "teacher_type_id")


class TeacherSerializer(common_serializer.CommonSerializer):

    city = common_serializer.CitySerializer()
    school = common_serializer.SchoolSerializer()
    subjects = serializers.ListField()
    teacher_types = serializers.ListField()
    follower_count = serializers.IntegerField()
    apply_count = serializers.IntegerField()
    confirms = serializers.ListField(required=True)
    learn_name = serializers.CharField()

    class Meta:
        model = models.Teacher
        fields = "__all__"


# create teacher

class CreateTeacherSubjectSerializer(serializers.ModelSerializer):
    """创建教师学科"""

    class Meta:
        model = models.TeacherSubjectsShip
        fields = ("id", "subject")


class CreateTeacherTypeSerializer(serializers.ModelSerializer):
    """创建教师特点"""

    class Meta:
        model = models.TeacherTypesShip
        fields = ("id", "teacher_type")


class CreateTeacherSerializer(serializers.ModelSerializer):
    """
        创建老师
    """

    subjects = serializers.ListField(required=True)
    teacher_types = serializers.ListField(required=True)
    confirms = serializers.ListField(required=True)

    class Meta:
        model = models.Teacher
        fields = "__all__"


# 修改教师

class UpdateTeacherSerializer(serializers.ModelSerializer):
    """
        修改教师
    """

    last_name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    school = serializers.CharField(required=False)
    subjects = serializers.ListField(required=False)
    teacher_types = serializers.ListField(required=False)
    confirms = serializers.ListField(required=False)

    class Meta:
        model = models.Teacher
        fields = "__all__"


# # 教师被收藏序列化
#
# class CreateTeacherFollowerSerializer(serializers.ModelSerializer):
#     """
#         收藏 教师
#     """
#
#     class Meta:
#         model = models.TeacherFollowers
#         fields = ('teacher', 'created_at', 'updated_at')
#
#
# # 教师被申请序列化
#
# class CreateTeacherApplySerializer(serializers.ModelSerializer):
#     """
#         申请 教师
#     """
#
#     class Meta:
#         model = models.TeacherApply
#         fields = '__all__'