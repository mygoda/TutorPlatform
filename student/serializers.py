# coding=utf-8

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models
from common import serializers as common_serializer


class StudentSerializer(serializers.ModelSerializer):

    city = common_serializer.CitySerializer()
    subject = common_serializer.SubjectSerializer()
    level = common_serializer.LevelSerializer()

    class Meta:
        model = models.Student
        fields = "__all__"


