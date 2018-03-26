# coding=utf-8

from rest_framework import serializers
from . import models
from common import serializers as common_serializer


class CustomerFavoriteSerializer(serializers.ModelSerializer):
    """
        用户收藏序列化
    """

    class Meta:
        model = models.CustomerFavorite
        fields = '__all__'


class GetCustomerFavoriteSerializer(serializers.ModelSerializer):
    """
        获取用户收藏 序列化
    """

    target_name = serializers.CharField()
    target_subject = serializers.ListField()
    target_is_valid = serializers.CharField()
    target_money = serializers.CharField()

    class Meta:
        model = models.CustomerFavorite
        fields = '__all__'


class CustomerApplySerializer(serializers.ModelSerializer):
    """
        用户收藏序列化
    """

    class Meta:
        model = models.CustomerApply
        fields = '__all__'


