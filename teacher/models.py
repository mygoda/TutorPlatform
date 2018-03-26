# coding=utf-8

from __future__ import unicode_literals

from django.db import models
from common import models as common_models
from libs import uuid
from common.const import Sex, FOLLOWER_TYPE, APPLY_TYPE
from .const import TEACHER_LEARN
from customer.models import Customer
from operation.models import CustomerFavorite, CustomerApply
# Create your models here.


class Teacher(common_models.CommonModel):
    """教师"""

    customer = models.ForeignKey(Customer, verbose_name="用户", null=True, blank=True)
    uid = models.CharField(u"教师ID", max_length=16, default=uuid.create_teacher_uid, unique=True)
    last_name = models.CharField(u"姓氏", max_length=4)
    city = models.ForeignKey(common_models.City, null=True, blank=True, default=1, verbose_name="城市")
    school = models.ForeignKey(common_models.School, verbose_name="学校")
    phone = models.CharField(u"电话", max_length=16)
    sex = models.IntegerField(u"性别", default=Sex.WOMEN, help_text="0：女 1：男")
    learn = models.ForeignKey(common_models.Learn, default=1, verbose_name="学历")
    profession = models.CharField(u"专业", max_length=32, null=True, blank=True)
    high_score = models.IntegerField(u"高考分数", default=0)
    money = models.IntegerField(u"期望薪资", default=0, help_text="默认单位：小时")
    is_valid = models.BooleanField(u"是否有效", default=True)
    head_image = models.CharField(u"头像", max_length=255, null=True, blank=True)
    self_introduction = models.CharField(u"自我介绍", max_length=1000, null=True, blank=True)

    def __unicode__(self):
        return "%s老师" % self.last_name

    @property
    def learn_name(self):
        return self.learn.name

    @property
    def subjects(self):
        return self.teachersubjectsship_set.all()

    @property
    def confirms(self):
        return [con.confirm for con in self.teacherconfirm_set.all()]

    @property
    def teacher_types(self):
        return self.teachertypesship_set.all()

    @property
    def follower_count(self):
        """
            收藏数
        :return:
        """
        return CustomerFavorite.objects.filter(is_valid=True, target_id=self.id, target_type='teacher').count()
        # return self.teacherfollowers_set.filter(is_valid=True).count()

    def followers(self):
        """
            收藏列表
        :return:
        """
        return CustomerFavorite.objects.filter(is_valid=True, target_id=self.id, target_type='teacher').all()
        # return self.teacherfollowers_set.filter(is_valid=True).all()

    def customer_is_follower(self, customer_id):
        return CustomerFavorite.objects.filter(is_valid=True, target_id=self.id, target_type='teacher', customer_id=customer_id).exists()
        # return self.teacherfollowers_set.filter(is_valid=True, customer_id=customer_id).exists()

    @classmethod
    def add_teacher(cls, **kwargs):
        """
            添加老师
        :return:
        """
        customer = kwargs.get("customer")
        # if not customer:
        #     customer = Customer.add()
        #     kwargs["customer"] = customer
        if customer.customer_type:
            return False, '用户已注册过角色'

        if not cls.objects.filter(phone=kwargs.get("phone"), is_valid=True).exists():

            subjects = kwargs.pop('subjects', [])
            confirms = kwargs.pop('confirms', [])
            teacher_types = kwargs.pop('teacher_types', [])

            teacher = cls(**kwargs)
            teacher.save(force_insert=True)
            # 添加教师 所教 科目
            for id in subjects:
                subject = {}
                subject["teacher"] = teacher
                subject["subject_id"] = int(id)
                teacher_subject = TeacherSubjectsShip(**subject)
                teacher_subject.save()

            # 添加教师 证书
            for id in confirms:
                confirm = {}
                confirm["teacher"] = teacher
                confirm["confirm"] = id
                teacher_confirm = TeacherConfirm(**confirm)
                teacher_confirm.save()

            # 添加教师 教学特点
            for id in teacher_types:
                teacher_type = {}
                teacher_type["teacher"] = teacher
                teacher_type["teacher_type_id"] = int(id)
                teacher_type_ship = TeacherTypesShip(**teacher_type)
                teacher_type_ship.save()

            # 变更用户角色
            if teacher.customer.change_type(1):
                return True, teacher.id
            return False, '用户变更教师失败'
        return False, '%s 已存在' % kwargs.get("phone")

    def delete_teacher(self):
        """
            删除教师
            将is_valid 置为Fasle
        :return:
        """
        if self.is_valid:
            self.is_valid = False
            self.save()

            self.customer.change_type()
        self.teachersubjectsship_set.all()

    def update_teacher(self, **kwargs):
        """
            修改教师
        :param kwargs:
        :return:
        """
        subjects = kwargs.pop('subjects', [])
        # teacher_types = kwargs.pop('teacher_types', [])
        # 添加教师 所教 科目,添加前删除以前的
        if subjects:
            self.teachersubjectsship_set.all().delete()
            for id in subjects:
                subject = {}
                subject["teacher"] = self
                subject["subject_id"] = int(id)
                teacher_subject = TeacherSubjectsShip(**subject)
                teacher_subject.save()
        # if teacher_types:
        Teacher.objects.filter(id=self.id).update(**kwargs)


class TeacherSubjectsShip(common_models.CommonModel):

    teacher = models.ForeignKey(Teacher, verbose_name=u"教师")
    subject = models.ForeignKey(common_models.Subject, verbose_name="学科", related_name="teacher_subject")

    def __unicode__(self):
        return "%s:%s" % (self.teacher.uid, self.subject.name)

    @property
    def subject_name(self):
        return self.subject.name


class TeacherConfirm(common_models.CommonModel):
    """
        教师证书
    """
    teacher = models.ForeignKey(Teacher, verbose_name=u"教师")
    confirm = models.CharField(u"证书", max_length=255, null=True, blank=True)

    def __unicode__(self):
        return "%s" % (self.teacher.uid, )


class TeacherTypesShip(common_models.CommonModel):

    teacher = models.ForeignKey(Teacher, verbose_name=u"教师")
    teacher_type = models.ForeignKey(common_models.TeacherType, verbose_name="教学特点")

    def __unicode__(self):
        return "%s:%s" % (self.teacher.uid, self.teacher_type.name)

    @property
    def teacher_type_name(self):
        return [self.teacher_type.name]


# class TeacherFollowers(common_models.CommonModel):
#     """
#         老师 被收藏关系表
#         目前仅支持学生收藏老师，老师之间不可以收藏
#     """
#
#     teacher = models.ForeignKey(Teacher, help_text=u"教师")
#     customer = models.ForeignKey(Customer, null=True, help_text=u"收藏用户")
#     follower_type = models.IntegerField(u"收藏者类型, 目前教师仅能被学生收藏", default=FOLLOWER_TYPE.STUDENT, help_text="1：老师 2：学生")
#     is_valid = models.BooleanField(u"是否有效", default=True)
#
#     class Meta:
#         verbose_name = u'被收藏老师'
#         verbose_name_plural = verbose_name
#
#
#     @classmethod
#     def add_teacher_follower(cls, **kwargs):
#         """
#             点击收藏 教师
#         :return:
#         """
#         msg = ''
#         teacher = kwargs.get("teacher")
#         customer = kwargs.get("customer")
#         # 教师不能收藏教师
#         if customer.customer_type != 2:
#             msg = '仅学生才能收藏教师'
#             return False, msg
#         if not cls.objects.filter(is_valid=True, teacher=teacher, customer=customer).exists():
#             student_follower = cls(**kwargs)
#             student_follower.save(force_insert=True)
#             return student_follower.id, msg
#         msg = '不能重复收藏'
#         return False, msg
#
#     def delete_teacher_follower(self):
#         """
#             删除 教师 收藏
#         :return:
#         """
#         if self.is_valid:
#             self.is_valid = False
#             self.save()
#
#
# class TeacherApply(common_models.CommonModel):
#     """
#         老师 被申请列表
#         目前仅支持 学生向老师申请
#     """
#
#     teacher = models.ForeignKey(Teacher, help_text=u"教师")
#     student = models.ForeignKey(Customer, null=True, help_text=u"申请者")
#     apply_type = models.IntegerField(u"申请者类型, 目前教师仅能被学生申请", default=APPLY_TYPE.STUDENT, help_text="1：老师 2：学生")
#     is_valid = models.BooleanField(u"是否有效", default=True)
#
#     class Meta:
#         verbose_name = u'老师被申请列表'
#         verbose_name_plural = verbose_name
