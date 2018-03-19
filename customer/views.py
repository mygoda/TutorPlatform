# coding=utf-8
"""
    用户api
"""

import logging

from django.shortcuts import render
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework import viewsets
from libs import uuid, upload
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
    
    @list_route(methods=["POST"])
    def upload_file(self, request):
        files = request.FILES
        up_file = files.get("file")
        size = up_file.size / 1000
        stream = up_file.read()
        file_name = up_file.name
        key = "%s%s" % (uuid.create_uuid(), up_file.name)
        result = upload.upload_stream_to_qiniu(key=key, data=stream)
        return Response({'url': result, "key": key, "size": size, "name": file_name})