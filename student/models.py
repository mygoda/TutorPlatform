# coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.

from common import models as common_models
from operation.models import CustomerFavorite, CustomerApply
from student import const
from common.const import Sex, FOLLOWER_TYPE, APPLY_TYPE
from customer.models import Customer
from libs import uuid


class Student(common_models.CommonModel):
    """学生"""

    customer = models.ForeignKey(Customer, verbose_name="用户", null=True, blank=True)
    uid = models.CharField(u"学生ID", max_length=16, default=uuid.create_student_uid, unique=True)
    city = models.ForeignKey(common_models.City, null=True, blank=True, default=1, verbose_name="城市")
    name = models.CharField(u"姓名", max_length=32)
    phone = models.CharField(u"电话", max_length=16)
    level = models.ForeignKey(common_models.Level, verbose_name="年级")
    baselevel = models.ForeignKey(common_models.BaseLevel, default=1, verbose_name="年级")
    basis = models.ForeignKey(common_models.Basis, default=1, verbose_name="学生基础")
    times = models.CharField(u"补习次数", default="一周一次", max_length=64, help_text="1：一周一次， 2：一周2次，依次内推，最大7次, 0: 面议")
    money = models.CharField(u"金钱", max_length=12, default="面议")
    sex = models.IntegerField(u"性别", default=Sex.WOMEN, help_text="0：女 1：男")
    head_image = models.CharField(u"头像", max_length=255, null=True, blank=True)

    # 对老师的要求
    require = models.ForeignKey(common_models.TeacherRequire, default=1, verbose_name="教师资质")
    teacher_sex = models.IntegerField(u"教师性别", default=Sex.WOMEN, help_text="0：女 1：男")

    # 地址
    address = models.CharField(u"上课地点", max_length=128)
    is_valid = models.BooleanField(u"是否有效", default=True)

    extra = models.CharField(u"其他", max_length=128, null=True, blank=True)

    def __unicode__(self):
        return self.name

    @property
    def created_time(self):
        return self.created_at.strftime('%Y-%m-%d')

    @property
    def updated_time(self):
        return self.updated_at.strftime('%Y-%m-%d')

    @property
    def subjects(self):
        return self.studentsubjectsship_set.all()

    @property
    def student_types(self):
        return self.studenttypesship_set.all()

    @property
    def teacher_types(self):
        return self.studentteachertypes_set.all()

    @property
    def follower_count(self):
        """
        收藏数
        :return:
        """
        return CustomerFavorite.objects.filter(is_valid=True, target_id=self.id, target_type='student').count()

    def customer_is_follower(self, customer_id):
        """
            是否被浏览者收藏
        :param customer_id:
        :return:
        """
        return CustomerFavorite.objects.filter(is_valid=True, target_id=self.id, target_type='student', customer_id=customer_id).exists()

    @classmethod
    def add_student(cls, **kwargs):
        """
            添加
        :return:
        """
        customer = kwargs.get("customer")
        if customer.customer_type:
            return False, '用户已注册过角色'

        if not cls.objects.filter(phone=kwargs.get("phone"), is_valid=True).exists():
            teacher_types = kwargs.pop('teacher_types', [])
            student_types = kwargs.pop('student_types', [])
            subjects = kwargs.pop('subjects', [])

            student = cls(**kwargs)
            student.save(force_insert=True)

            # 添加学生对教师的要求 教学特点
            for id in teacher_types:
                teacher_type = {}
                teacher_type["student"] = student
                teacher_type["teacher_type_id"] = id
                teacher_type_ship = StudentTeacherTypes(**teacher_type)
                teacher_type_ship.save()

            # 添加学生的不足 学生不足
            for id in student_types:
                student_type = {}
                student_type["student"] = student
                student_type["student_type_id"] = id
                student_type_ship = StudentTypesShip(**student_type)
                student_type_ship.save()

            # 添加学生 所教 科目
            for id in subjects:
                subject = {}
                subject["student"] = student
                subject["subject_id"] = int(id)
                student_subject = StudentSubjectsShip(**subject)
                student_subject.save()
            # 变更用户角色
            if student.customer.change_type(2):
                return True, student.id
            return False, '用户变更学生失败'
        return False, '%s 已存在' % kwargs.get("phone")

    def delete_student(self):
        """
            删除
            将is_valid 置为Fasle
        :return:
        """
        if self.is_valid:
            self.is_valid = False
            self.save()

            self.customer.change_type()
        return True

    def update_student(self, **kwargs):
        """
            修改学生
        :param kwargs:
        :return:
        """
        subjects = kwargs.pop('subjects', [])
        if subjects:
            self.studentsubjectsship_set.all().delete()
            for id in subjects:
                subject = {}
                subject["student"] = self
                subject["subject_id"] = int(id)
                student_subject = StudentSubjectsShip(**subject)
                student_subject.save()
        Student.objects.filter(id=self.id).update(**kwargs)


class StudentSubjectsShip(common_models.CommonModel):

    student = models.ForeignKey(Student, verbose_name=u"学生")
    subject = models.ForeignKey(common_models.Subject, verbose_name="学科", related_name="student_subject")

    def __unicode__(self):
        return "%s:%s" % (self.teacher.uid, self.subject.name)

    @property
    def subject_name(self):
        return [self.subject.name]

    @property
    def subject_id(self):
        return [self.subject.id]


class StudentTeacherTypes(common_models.CommonModel):
    """
        学生 需求老师特点
    """

    student = models.ForeignKey(Student, verbose_name=u"学生")
    teacher_type = models.ForeignKey(common_models.TeacherType, verbose_name="教学特点")

    def __unicode__(self):
        return "%s:%s" % (self.student.uid, self.teacher_type.name)

    @property
    def teacher_type_name(self):
        return [self.teacher_type.name]

    @property
    def teacher_type_id(self):
        return [self.teacher_type.id]


class StudentTypesShip(common_models.CommonModel):

    student = models.ForeignKey(Student, verbose_name=u"学生")
    student_type = models.ForeignKey(common_models.StudentType, verbose_name="存在问题")

    def __unicode__(self):
        return "%s:%s" % (self.student.uid, self.student_type.name)

    @property
    def student_type_name(self):
        return [self.student_type.name]

    @property
    def student_type_id(self):
        return [self.student_type.id]


# class StudentFollowers(common_models.CommonModel):
#     """
#         学生 被收藏关系表
#         目前仅支持老师收藏学生，学生之间不可以收藏
#     """
#
#     student = models.ForeignKey(Student, help_text=u"学生")
#     customer = models.ForeignKey(Customer, null=True, help_text=u"收藏用户")
#     follower_type = models.IntegerField(u"收藏者类型，目前学生仅能被教师收藏", default=FOLLOWER_TYPE.TEACHER, help_text="1：老师 2：学生")
#     is_valid = models.BooleanField(u"是否有效", default=True)
#
#     class Meta:
#         verbose_name = u'被收藏学生'
#         verbose_name_plural = verbose_name
#
#     @classmethod
#     def add_student_follower(cls, **kwargs):
#         """
#             点击收藏学生
#         :return:
#         """
#         msg = ''
#         student = kwargs.get("student")
#         customer = kwargs.get("customer")
#         if customer.customer_type != 1:
#             msg = '仅教师才能收藏学生'
#             return False, msg
#         if not cls.objects.filter(is_valid=True, student=student, customer=customer).exists():
#             student_follower = StudentFollowers(**kwargs)
#             student_follower.save(force_insert=True)
#             return student_follower.id, msg
#         msg = '不能重复收藏'
#         return False, msg
#
#     def delete_student_follower(self):
#         """
#             删除 学生 收藏
#         :return:
#         """
#         if self.is_valid:
#             self.is_valid = False
#             self.save()
#
#
# class StudentrApply(common_models.CommonModel):
#     """
#         老师 被申请列表
#         目前仅支持 学生向老师申请
#     """
#
#     student = models.ForeignKey(Student, help_text=u"学生")
#     customer = models.ForeignKey(Customer, null=True, help_text=u"申请者")
#     apply_type = models.IntegerField(u"申请者类型, 目前教师仅能被学生申请", default=APPLY_TYPE.TEACHER, help_text="1：老师 2：学生")
#     is_valid = models.BooleanField(u"是否有效", default=True)
#
#     class Meta:
#         verbose_name = u'老师被申请列表'
#         verbose_name_plural = verbose_name
