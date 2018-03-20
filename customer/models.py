# coding=utf-8

from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models
from libs.uuid import create_uuid
# Create your models here.
import time
from django.conf import settings
from common import models as common_models


class Customer(common_models.CommonModel):
    """用户"""
    USER_TYPE = (
        (0, '没有注册'),
        (1, '教师'),
        (2, '学生')
    )

    # user = models.OneToOneField(User)
    uuid = models.CharField(u"微信ID", max_length=64, unique=True)
    nickname = models.CharField(u"微信名称", max_length=64, null=True, blank=True)
    avatar_url = models.URLField("头像", help_text="头像", null=True, blank=True)
    customer_type = models.IntegerField(u"用户角色", choices=USER_TYPE, default=0, help_text='0: 没有注册 1: 教师 2: 学生')

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    @property
    def user_type(self):
        if self.customer_type == 1:
            return '教师'
        elif self.customer_type == 2:
            return '学生'
        else:
            return '未注册'

    @property
    def user_favorites(self):
        if self.customer_type == 1:
            # 当用户为教师时，只显示收藏的学生
            student_followers = []
            for follower in self.studentfollowers_set.filter(is_valid=True):
                student = {}
                student['id'] = follower.id
                student['student_id'] = follower.student.id
                student['student_name'] = follower.student.name
                student['student_is_valid'] = follower.student.is_valid
                student['student_subject'] = [{"name": subject.subject.name} for subject in follower.student.studentsubjectsship_set.all()]
                student_followers.append(student)
            return student_followers
        elif self.customer_type == 2:
            # 当用户为学生时，只显示收藏的教师
            teacher_followers = []
            for follower in self.teacherfollowers_set.filter(is_valid=True):
                teacher = {}
                teacher['id'] = follower.id
                teacher['teacher_id'] = follower.teacher.id
                teacher['teacher_name'] = follower.teacher.last_name
                teacher['teacher_is_valid'] = follower.teacher.is_valid
                teacher['teacher_subject'] = [{"name": subject.subject.name} for subject in follower.teacher.teachersubjectsship_set.all()]
                teacher_followers.append(teacher)
            return teacher_followers
        else:
            return []

    @property
    def user_apply(self):
        """
            我的申请
        :return:
        """
        self_apply = []
        if self.customer_type == 1:
            # 当用户为教师时，只能被学生申请
            for apply in self.teacherapply_set.filter(is_valid=True):
                student = apply.customer.student_set.filter(is_valid=True).first()
                student_apply = {}
                student_apply['id'] = apply.id
                student_apply['student_id'] = student.id
                student_apply['student_name'] = student.name
                student_apply['student_money'] = student.money
                student_apply['student_is_valid'] = student.is_valid
                student_apply['student_subject'] = [{"name": subject.subject.name} for subject in student.studentsubjectsship_set.all()]
                self_apply.append(student_apply)
        elif self.customer_type == 2:
            # 当用户为学生时，只能被教师申请
            for apply in self.studentrapply_set.filter(is_valid=True):
                teacher = apply.customer.teacher_set.filter(is_valid=True).first()
                teacher_apply = {}
                teacher_apply['id'] = apply.id
                teacher_apply['teacher_id'] = teacher.id
                teacher_apply['teacher_name'] = teacher.last_name
                teacher_apply['teacher_money'] = teacher.money
                teacher_apply['student_subject'] = [{"name": subject.subject.name} for subject in teacher.teachersubjectsship_set.all()]
                self_apply.append(teacher_apply)
        return self_apply

    def change_type(self, user_type=0):
        """
            变更 用户身份
        :param type:
        :return:
        """
        if not self.customer_type:
            self.customer_type = int(user_type)
            self.save()
            return self.id
        if self.customer_type and not user_type:
            self.customer_type = 0
            self.save()


    @classmethod
    def add(cls):
        from libs.uuid import create_uuid
        kwargs = {
            "uuid": create_uuid(),
            "nickname": 'customer'
        }
        cus = cls(**kwargs)
        cus.save()
        return cus


class CustomerTokenShip(common_models.CommonModel):

    customer = models.ForeignKey(Customer, verbose_name="用户")
    token = models.CharField(u"TOKEN", max_length=36, default=create_uuid)
    expire_time = models.IntegerField(u"超时时间", default=0)

    def __unicode__(self):
        return self.customer.nickname

    @classmethod
    def new_customer_token(cls, customer_id):
        max_expire_time = settings.TOKEN_EXPIRE_TIME + time.time()
        customer_token = cls(customer_id=customer_id, expire_time=max_expire_time)
        customer_token.save()
        return customer_token.token

    @classmethod
    def get_customer_by_token(cls, token):
        """根据token获取用户"""
        now = time.time()
        customer_tokens = cls.objects.filter(token=token, expire_time__gt=now)
        if customer_tokens.exists():
            return customer_tokens[0].customer
        else:
            return None
