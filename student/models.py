# coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.

from common import models as common_models
from student import const
from common.const import Sex
from customer.models import Customer
from libs import uuid


class Student(common_models.CommonModel):
    """学生"""

    customer = models.ForeignKey(Customer, verbose_name="用户", null=True, blank=True)
    uid = models.CharField(u"学生ID", max_length=16, default=uuid.create_student_uid, unique=True)
    city = models.ForeignKey(common_models.City, verbose_name="城市")
    name = models.CharField(u"姓名", max_length=32)
    phone = models.CharField(u"电话", max_length=16)
    level = models.ForeignKey(common_models.Level, verbose_name="年级")
    subject = models.ForeignKey(common_models.Subject, verbose_name="学科")
    study = models.CharField(u"学习情况", max_length=32, null=True, blank=True)
    times = models.IntegerField(u"补习次数", default=1, help_text="1：一周一次， 2：一周2次，依次内推，最大7次, 0: 面议")
    money = models.CharField(u"金钱", max_length=12, default="面议")
    sex = models.IntegerField(u"性别", default=Sex.WOMEN, help_text="0：女 1：男")

    # 对老师的要求
    require = models.CharField(u"教师资质", max_length=32, default="不限")
    teacher_sex = models.IntegerField(u"教师性别", default=Sex.WOMEN, help_text="0：女 1：男")

    # 地址
    address = models.CharField(u"上课地点", max_length=128)
    is_valid = models.BooleanField(u"是否有效", default=True)

    extra = models.CharField(u"其他", max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.name

    @classmethod
    def add_student(cls, **kwargs):
        """
            添加
        :return:
        """

        teacher_types = kwargs.pop('teacher_types')
        student_types = kwargs.pop('student_types')

        student = cls(**kwargs)
        student.save(force_insert=True)

        # 添加学生对教师的要求 教学特点
        for teacher_type in teacher_types:
            teacher_type["student"] = student
            teacher_type_ship = StudentTeacherTypes(**teacher_type)
            teacher_type_ship.save()

        # 添加学生的不足 学生不足
        for student_type in student_types:
            student_type["student"] = student
            student_type_ship = StudentTypesShip(**student_type)
            student_type_ship.save()
        return student.id

    def delete_student(self):
        """
            删除
            将is_valid 置为Fasle
        :return:
        """
        if self.is_valid:
            self.is_valid = False
            self.save()
        return


class StudentTeacherTypes(common_models.CommonModel):
    """
        学生 需求老师特点
    """

    student = models.ForeignKey(Student, verbose_name=u"学生")
    teacher_type = models.ForeignKey(common_models.TeacherType, verbose_name="教学特点")

    def __unicode__(self):
        return "%s:%s" % (self.student.uid, self.teacher_type.name)


class StudentTypesShip(common_models.CommonModel):

    student = models.ForeignKey(Student, verbose_name=u"学生")
    student_type = models.ForeignKey(common_models.StudentType, verbose_name="存在问题")

    def __unicode__(self):
        return "%s:%s" % (self.student.uid, self.student_type.name)
