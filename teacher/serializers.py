# coding=utf-8

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models
from common import serializers as common_serializer


class TeacherSubjectSerializer(serializers.ModelSerializer):
    """教师学科"""

    # subject = common_serializer.SubjectSerializer()

    class Meta:
        model = models.TeacherSubjectsShip
        fields = ("id", "subject")


class TeacherSerializer(serializers.ModelSerializer):

    city = common_serializer.CitySerializer()
    school = common_serializer.SchoolSerializer()
    subjects = TeacherSubjectSerializer(many=True)

    class Meta:
        model = models.Teacher
        fields = "__all__"


class CreateTeacherSerializer(serializers.ModelSerializer):
    """
        创建老师
    """

    subjects = TeacherSubjectSerializer(many=True)

    class Meta:
        model = models.Teacher
        fields = "__all__"