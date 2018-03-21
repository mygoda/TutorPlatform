# coding=utf-8

from django.contrib.auth.models import User, Group
from rest_framework import serializers
from . import models


class CustomerSerializer(serializers.ModelSerializer):
    """
        用户序列化
    """

    user_favorites = serializers.ListField()
    user_apply = serializers.ListField()
    user_type = serializers.CharField()

    class Meta:
        model = models.Customer
        fields = ('user_type', 'uuid', 'nickname', 'avatar_url', 'user_favorites', 'user_apply')


class CustomerSuggestionSerializer(serializers.ModelSerializer):
    """
        投诉序列化
    """

    class Meta:
        model = models.CustomerSuggestion
        fields = '__all__'