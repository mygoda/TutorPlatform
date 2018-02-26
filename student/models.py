# coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.

from common import models as common_models
from student import const
from common.const import Sex
from libs import uuid


class Student(common_models.CommonModel):
    """学生"""

    uid = models.CharField(u"学生ID", max_length=16, default=uuid.create_student_uid, unique=True)
    city = models.ForeignKey(common_models.City, verbose_name="城市")
    name = models.CharField(u"姓名", max_length=32)
    phone = models.CharField(u"电话", max_length=16)
    level = models.ForeignKey(common_models.Level, verbose_name="年级")
    subject = models.ForeignKey(common_models.Subject, verbose_name="学科")
    study = models.CharField(u"学习情况", max_length=32, null=True, blank=True)
    times = models.IntegerField(u"补习次数", default=1, help_text="1：一周一次， 2：一周2次，依次内推，最大7次, 0: 面议")
    money = models.CharField(u"金钱", max_length=12, default="面议")

    # 对老师的要求
    require = models.CharField(u"教师资质", max_length=32, default="不限")
    sex = models.IntegerField(u"性别要求", default=Sex.WOMEN, help_text="0：女 1：男")

    # 地址
    address = models.CharField(u"上课地点", max_length=128)
    id_valid = models.BooleanField(u"是否有效", default=True)

    extra = models.CharField(u"其他", max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.name





