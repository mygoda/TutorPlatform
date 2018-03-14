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
    customer_type = models.IntegerField(u"用户角色", choices=USER_TYPE, default=0, help_text='0: 没有注册 1: 教师 2: 学生')

    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

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
                student['student_subject'] = follower.student.subject.name
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
                teacher['teacher_subject'] = [{"name": subject.subject.name} for subject in follower.teacher.teachersubjectsship_set.all()]
                teacher_followers.append(teacher)
            return teacher_followers
        else:
            return []

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