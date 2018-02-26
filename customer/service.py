# coding=utf-8
from django.contrib.auth.models import User


def register_django_user(uuid):
    """注册django用户"""
    user, created = User.objects.get_or_create(username=uuid)
    return user