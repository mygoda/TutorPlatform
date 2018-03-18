# coding=utf-8

from rest_framework import serializers
from . import models


class CitySerializer(serializers.ModelSerializer):
    """
        城市 序列化
    """

    class Meta:
        model = models.City
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):
    """
        科目 序列化
    """

    class Meta:
        model = models.Subject
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):
    """
        年级 序列化
    """

    # base = BaseLevelSerializer()

    class Meta:
        model = models.Level
        fields = "__all__"


class BaseLevelSerializer(serializers.ModelSerializer):
    """
        学校等级,年级 序列化
    """

    level = LevelSerializer(many=True)

    class Meta:
        model = models.BaseLevel
        fields = "__all__"


class BaseSchoolSerializer(serializers.ModelSerializer):
    """
        学校等级 序列化
    """

    class Meta:
        model = models.BaseLevel
        fields = ('id', 'name')


class BasisSerializer(serializers.ModelSerializer):
    """
        学生基础 序列化
    """

    class Meta:
        model = models.Basis
        fields = "__all__"


class LearnSerializer(serializers.ModelSerializer):
    """
        学历 序列化
    """

    class Meta:
        model = models.Learn
        fields = "__all__"


class SchoolSerializer(serializers.ModelSerializer):
    """
        学校 序列化
    """

    city = CitySerializer()

    class Meta:
        model = models.School
        fields = "__all__"


class TeacherTypeSerializer(serializers.ModelSerializer):
    """
        教师特点 序列化
    """

    class Meta:
        model = models.TeacherType
        fields = "__all__"


class StudentTypeSerializer(serializers.ModelSerializer):
    """
        学生不足 序列化
    """

    class Meta:
        model = models.StudentType
        fields = "__all__"


class TeacherRequireSerializer(serializers.ModelSerializer):
    """
        教师特点 序列化
    """

    class Meta:
        model = models.TeacherRequire
        fields = "__all__"