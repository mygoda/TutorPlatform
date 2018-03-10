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
    high_score = models.IntegerField(u"高考分数", default=0)
    money = models.IntegerField(u"期望薪资", default=0, help_text="默认单位：小时")
    is_valid = models.BooleanField(u"是否有效", default=True)
    head_image = models.CharField(u"头像", max_length=255, null=True, blank=True)
    self_introduction = models.CharField(u"自我介绍", max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return "%s老师" % self.last_name

    @property
    def subjects(self):
        return self.teachersubjectsship_set.all()

    @classmethod
    def add_teacher(cls, **kwargs):
        """
            添加老师
        :return:
        """
        subjects = kwargs.pop('subjects')
        teacher_types = kwargs.pop('teacher_types')

        teacher = cls(**kwargs)
        teacher.save(force_insert=True)
        # 添加教师 所教 科目
        for subject in subjects:
            subject["teacher"] = teacher
            teacher_subject = TeacherSubjectsShip(**subject)
            teacher_subject.save()

        # 添加教师 教学特点
        for teacher_type in teacher_types:
            teacher_type["teacher"] = teacher
            teacher_type_ship = TeacherTypesShip(**teacher_type)
            teacher_type_ship.save()

        return teacher.id

    def delete_teacher(self):
        """
            删除教师
            将is_valid 置为Fasle
        :return:
        """
        if self.is_valid:
            self.is_valid = False
            self.save()
        return

class TeacherSubjectsShip(common_models.CommonModel):

    teacher = models.ForeignKey(Teacher, verbose_name=u"教师")
    subject = models.ForeignKey(common_models.Subject, verbose_name="学科", related_name="teacher_subject")

    def __unicode__(self):
        return "%s:%s" % (self.teacher.uid, self.subject.name)


class TeacherTypesShip(common_models.CommonModel):

    teacher = models.ForeignKey(Teacher, verbose_name=u"教师")
    teacher_type = models.ForeignKey(common_models.TeacherType, verbose_name="教学特点")

    def __unicode__(self):
        return "%s:%s" % (self.teacher.uid, self.teacher_type.name)

