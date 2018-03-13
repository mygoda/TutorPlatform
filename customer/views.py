# coding=utf-8
"""
    用户api
"""

import logging

from django.shortcuts import render
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from rest_framework import viewsets

from . import models as customer_models
from . import serializers as customer_serializers

logger = logging.getLogger(__name__)
# Create your views here.


class CustomerViewset(viewsets.ModelViewSet):
    """
        用户 api
    """

    def get_queryset(self):
        return customer_models.Customer.objects.all()

    def get_serializer_class(self):
        """
            获取序列化
        :return:
        """

        return customer_serializers.CustomerSerializer
