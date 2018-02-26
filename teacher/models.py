# coding=utf-8

from __future__ import unicode_literals

from django.db import models
from common import models as common_models
from libs import uuid
from common.const import Sex
from .const import TEACHER_LEARN
from customer.models import Customer
# Create your models here.


class Teacher(common_models.CommonModel):
    """教师"""

    customer = models.ForeignKey(Customer, verbose_name="用户", null=True, blank=True)
    uid = models.CharField(u"教师ID", max_length=16, default=uuid.create_teacher_uid, unique=True)
    last_name = models.CharField(u"姓氏", max_length=4)
    city = models.ForeignKey(common_models.City, verbose_name="城市")
    school = models.ForeignKey(common_models.School, verbose_name="学校")
    phone = models.CharField(u"电话", max_length=16)
    sex = models.IntegerField(u"性别", default=Sex.WOMEN, help_text="0：女 1：男")
    learn = models.IntegerField("学历", default=0, choices=TEACHER_LEARN)
    profession = models.CharField(u"专业", max_length=32, null=True, blank=True)
    money = models.IntegerField(u"期望薪资", default=0, help_text="默认单位：小时")
    is_valid = models.BooleanField(u"是否有效", default=True)
    head_image = models.CharField(u"头像", max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "%s老师" % self.last_name

    @property
    def subjects(self):
        return self.teachersubjectsship_set.all()


class TeacherSubjectsShip(common_models.Subject):

    teacher = models.ForeignKey(Teacher, verbose_name=u"教师")
    subject = models.ForeignKey(common_models.Subject, verbose_name="学科", related_name="teacher_subject")

    def __unicode__(self):
        return "%s:%s" % (self.teacher.uid, self.subject.name)

