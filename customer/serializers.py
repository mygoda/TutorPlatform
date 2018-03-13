# coding=utf-8

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models


class CustomerSerializer(serializers.ModelSerializer):
    """
        用户序列化
    """

    user_favorites = serializers.CharField()

    class Meta:
        model = models.Customer
        fields = '__all__'


