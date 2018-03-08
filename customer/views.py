# coding=utf-8
"""
    用户api
"""

import logging

from django.shortcuts import render

from rest_framework.response import Response
from rest_framework import viewsets

from . import models as customer_models
from . import serializers as customer_serializers

logger = logging.getLogger(__name__)
# Create your views here.


class FavoriteViewset(viewsets.ModelViewSet):
    """
       用户 收藏 api
    """

    def get_queryset(self):
        return customer_models.UserFavorite.objects.filter()

    def get_serializer_class(self):
        """
            获取 收藏 序列化
        :return:
        """
        if self.action == 'action':
            return customer_serializers.FavoriteSerializer
        else:
            return customer_serializers.FavoriteSerializer

    def create(self, request, *args, **kwargs):
        """
            点击收藏
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        user_id = params.get('user_id')
        print('start add user %s favorite info %s' % (user_id, params))
        pass
