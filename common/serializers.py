# coding=utf-8

from rest_framework import serializers
from . import models


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.City
        fields = "__all__"


class SubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Subject
        fields = "__all__"


class BaseLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BaseLevel
        fields = "__all__"


class LevelSerializer(serializers.ModelSerializer):

    base = BaseLevelSerializer()

    class Meta:
        model = models.Level
        fields = "__all__"