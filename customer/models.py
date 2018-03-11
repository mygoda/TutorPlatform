# coding=utf-8

from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.
from common import models as common_models


class Customer(common_models.CommonModel):
    """用户"""
    USER_TYPE = (
        (0, '没有注册'),
        (1, '教师'),
        (2, '学生')
    )

    user = models.OneToOneField(User)
    uuid = models.CharField(u"微信ID", max_length=64, unique=True)
    nickname = models.CharField(u"微信名称", max_length=64, null=True, blank=True)
    avatar_url = models.URLField("头像", help_text="头像", null=True, blank=True)
    customer_type = models.IntegerField(u"用户角色", choices=USER_TYPE, default=1, help_text='0: 没有注册 1: 教师 2: 学生')

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    @property
    def user_favorite(self):
        if self.customer_type == 1:
            return self.teacher_set.first().followers()
        elif self.customer_type == 2:
            return self.student_set.first().followers()
