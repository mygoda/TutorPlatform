# -*- coding: utf-8 -*-
"""
    家教老师 api
"""
import logging

from rest_framework.response import Response
from rest_framework import viewsets

from common.exe import TokenException
from . import serializers as operation_serializers
from . import models as operation_models

logger = logging.getLogger(__name__)


class CustomerFavoriteViewset(viewsets.ModelViewSet):
    """
        用户收藏 api
    """

    def get_queryset(self):
        return operation_models.CustomerFavorite.objects.filter(is_valid=True)

    def get_serializer_class(self):
        if self.action == 'create':
            return operation_serializers.CustomerFavoriteSerializer
        elif self.action == 'list':
            return operation_serializers.GetCustomerFavoriteSerializer
        else:
            return operation_serializers.CustomerFavoriteSerializer

    def create(self, request, *args, **kwargs):
        """
            增加收藏
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        data = request.data
        customer = request.customer
        if not customer:
            raise TokenException('用户验证失败')
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        params = serializer.validated_data
        params['customer'] = customer
        logger.info("customer %s add favorite params %s" % (customer.id, params))
        fav_id, msg = operation_models.CustomerFavorite.add_favorite(**params)
        if fav_id:
            return Response({'status': 1, 'fav_id': fav_id})
        logger.info("add favorite error %s params: %s" % (msg, params))
        return Response({'status': 0, 'msg': msg})

    def list(self, request, *args, **kwargs):
        """
            获取用户收藏列表
        :param request:
        :param args:
        :param kwargs:{
	        "target_id": 6,
	        "target_type": "student"
        }
        :return:
        """
        customer = request.customer
        if not customer:
            raise TokenException('用户验证失败')
        queryset = self.get_queryset()
        if customer.customer_type == 1:
            # 当用户角色为教师时，获取他收藏的学生
            queryset = queryset.filter(customer_id=customer.id, target_type='student')
        elif customer.customer_type == 2:
            # 当用户角色为学生时，获取他收藏的教师
            queryset = queryset.filter(customer_id=customer.id, target_type='teacher')
        else:
            # 用户为注册
            return Response({'status': 0, 'msg': '用户未注册'})
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
            删除 收藏
        :param request:
        :param pk: 收藏id
        :return:
        """
        logger.info('start delete customer follower %s' % pk)
        customer_fav = operation_models.CustomerFavorite.objects.get(id=pk)
        if request.customer != customer_fav.customer:
            raise TokenException('用户验证失败')
        customer_fav.delete_favorite()
        logger.info('customer %s delete favorite %s success' % (customer_fav.customer_id, pk))
        return Response({'status': 1, 'id': pk})



