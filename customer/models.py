# coding=utf-8

from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
from common import models as common_models


class Customer(common_models.CommonModel):
    """用户"""

    user = models.OneToOneField(User)
    uuid = models.CharField(u"微信ID", max_length=64, unique=True)
    nickname = models.CharField(u"微信名称", max_length=64, null=True, blank=True)
    avatar_url = models.URLField("头像", help_text="头像", null=True, blank=True)

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name


class UserFavorite(common_models.CommonModel):
    """
        用户收藏
    """

    FAV_TYPE = (
        (1, '教师'),
        (2, '学生')
    )

    user = models.ForeignKey(Customer, help_text='用户')
    fav_id = models.IntegerField(default=0, help_text='被收藏者id')
    fav_type = models.IntegerField(choices=FAV_TYPE, default=1, help_text='1: 教师 2: 学生')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name


class UserRequest(common_models.CommonModel):
    """
        用户申请
    """

    REQ_TYPE = (
        (1, '教师'),
        (2, '学生')
    )

    user = models.ForeignKey(Customer, help_text='用户')
    req_id = models.IntegerField(default=0, help_text='被申请者id')
    req_type = models.IntegerField(choices=REQ_TYPE, default=1, help_text='1: 教师 2: 学生')

    class Meta:
        verbose_name = u'用户申请'
        verbose_name_plural = verbose_name