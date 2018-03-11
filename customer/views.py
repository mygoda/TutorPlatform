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

