# coding=utf-8

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models
from common import serializers as common_serializer


# get student serializer

class StudentSubjectSerializer(serializers.ModelSerializer):
    """教师学科"""

    subject_name = serializers.CharField()

    class Meta:
        model = models.StudentSubjectsShip
        fields = ("id", "subject_name", "subject_id")


class StudentTypeSerializer(serializers.ModelSerializer):
    """ 学生的不足"""

    student_type_name = serializers.CharField()

    class Meta:
        model = models.StudentTypesShip
        fields = ("id", "student_type_name", "student_type_id")


class StudentTeacherTypeSerializer(serializers.ModelSerializer):
    """学生对教室要求 教师特点"""

    teacher_type_name = serializers.CharField()

    class Meta:
        model = models.StudentTeacherTypes
        fields = ("id", "teacher_type_name", "teacher_type_id")


class StudentSerializer(common_serializer.CommonSerializer):

    city = common_serializer.CitySerializer()
    subjects = StudentSubjectSerializer(many=True)
    level = common_serializer.LevelSerializer()
    basis = common_serializer.BasisSerializer()
    baselevel = common_serializer.BaseSchoolSerializer()
    require = common_serializer.TeacherRequireSerializer()
    student_types = StudentTypeSerializer(many=True)
    teacher_types = StudentTeacherTypeSerializer(many=True)
    follower_count = serializers.IntegerField()
    apply_count = serializers.IntegerField()
    created_time = serializers.CharField()
    updated_time = serializers.CharField()

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
    subjects = serializers.ListField(required=True)
    student_types = serializers.ListField(required=True)
    teacher_types = serializers.ListField(required=True)
    class Meta:
        model = models.Student
        fields = "__all__"


# 修改学生

class UpdateStudentSerializer(serializers.ModelSerializer):
    """
        修改学生
    """

    name = serializers.CharField(required=False)
    phone = serializers.CharField(required=False)
    level = serializers.CharField(required=False)
    baselevel = serializers.CharField(required=False)
    subjects = serializers.ListField(required=False)
    address = serializers.CharField(required=False)

    class Meta:
        model = models.Student
        fields = "__all__"


# # 学生被收藏序列化
#
# class CreateStudentFollowerSerializer(serializers.ModelSerializer):
#     """
#         收藏学生
#     """
#
#     class Meta:
#         model = models.StudentFollowers
#         fields = ('student', 'created_at', 'updated_at')
