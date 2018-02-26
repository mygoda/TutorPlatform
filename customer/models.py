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

    def __unicode__(self):
        return self.uuid
