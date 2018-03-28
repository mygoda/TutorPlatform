# -*- coding: utf-8 -*-
"""
    用户操作 app model
"""

import logging

from django.contrib.contenttypes.models import ContentType
from django.db import models

from common import models as common_models
from customer import models as customer_models


TARGET_TYPE = ['teacher', 'student']

USER_TYPE = {
    0: 'no',
    1: 'teacher',
    2: 'student'
}

CHECK_FAV = {
    0: ['ours', '您尚未注册'],
    1: ['student', '仅学生才能收藏教师'],
    2: ['teacher', '仅教师才能收藏学生']
}

CHECK_APPLY = {
    0: ['ours', '您尚未注册'],
    1: ['student', '仅学生才能申请教师'],
    2: ['teacher', '仅教师才能申请学生']
}


class CustomerFavorite(common_models.CommonModel):
    """
        用户的收藏
    """

    customer = models.ForeignKey(customer_models.Customer, null=True, blank=True, verbose_name=u'用户')
    target_id = models.IntegerField(default=0, verbose_name=u'收藏对象id')
    target_type = models.CharField(max_length=64, verbose_name=u'收藏对象')
    is_valid = models.BooleanField(u"是否有效", default=True)
    customer_type = models.CharField(max_length=64, null=True, blank=True, verbose_name=u'用户收藏时身份')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name

    @property
    def target_name(self):
        """
            收藏对象 name
        :return:
        """
        target_obj = self.get_target_obj()
        if target_obj.customer.customer_type == 1:
            return target_obj.last_name
        elif target_obj.customer.customer_type == 2:
            return target_obj.name

    @property
    def target_subject(self):
        """
         收藏对象  科目
        :return:
        """
        target_obj = self.get_target_obj()
        if target_obj.customer.customer_type == 1:
            return [subject.subject.name for subject in target_obj.teachersubjectsship_set.all()]
        elif target_obj.customer.customer_type == 2:
            return [subject.subject.name for subject in target_obj.studentsubjectsship_set.all()]

    @property
    def target_is_valid(self):
        """
            收藏对象  是否有效
        :return:
        """
        return self.get_target_obj().is_valid

    @property
    def target_money(self):
        """
            收藏对象  是否有效
        :return:
        """
        return self.get_target_obj().money

    @classmethod
    def add_favorite(cls, **kwargs):
        """
            点击收藏
        :return:
        """
        msg = ''
        customer = kwargs.get("customer")
        target_type = kwargs.get("target_type")
        target_id = kwargs.get("target_id")
        # 判断用户身份能否收藏
        check = CHECK_FAV.get(customer.customer_type)
        if target_type not in TARGET_TYPE or check[0] != target_type:
            msg = check[-1]
            return False, msg
        if not cls.objects.filter(is_valid=True, target_type=target_type, target_id=target_id, customer=customer).exists():
            kwargs['customer_type'] = USER_TYPE.get(customer.customer_type)
            fav = cls(**kwargs)
            fav.save(force_insert=True)
            return fav.id, msg
        msg = '不能重复收藏'
        return False, msg

    def delete_favorite(self):
        """
            删除
        :return:
        """
        if self.is_valid:
            self.is_valid = False
            self.save()


class CustomerApply(common_models.CommonModel):
    """
        用户的申请
    """

    target_customer = models.ForeignKey(customer_models.Customer, null=True, blank=True, verbose_name=u'申请对象用户')
    target_id = models.IntegerField(default=0, verbose_name=u'申请对象id')
    target_type = models.CharField(max_length=64, null=True, blank=True, verbose_name=u'申请对象类型')
    is_valid = models.BooleanField(u"是否有效", default=True)
    apply_type = models.CharField(max_length=64, null=True, blank=True, verbose_name=u'申请者当时身份')
    apply_type_id = models.IntegerField(default=0, verbose_name=u'申请者当时身份id, 教师 or 学生')
    apply_customer_id = models.IntegerField(null=True, blank=True, verbose_name=u'申请者用户id')

    class Meta:
        verbose_name = u'用户申请'
        verbose_name_plural = verbose_name

    @property
    def target_name(self):
        """
            申请者 name
        :return:
        """
        target_obj = self.get_apply_obj()
        if target_obj.customer.customer_type == 1:
            return target_obj.last_name
        elif target_obj.customer.customer_type == 2:
            return target_obj.name

    @property
    def target_subject(self):
        """
         申请者  科目
        :return:
        """
        target_obj = self.get_apply_obj()
        if target_obj.customer.customer_type == 1:
            return [subject.subject.name for subject in target_obj.teachersubjectsship_set.all()]
        elif target_obj.customer.customer_type == 2:
            return [subject.subject.name for subject in target_obj.studentsubjectsship_set.all()]

    @property
    def target_is_valid(self):
        """
            申请对象  是否有效
        :return:
        """
        return self.get_apply_obj().is_valid

    @property
    def target_money(self):
        """
            收藏对象  是否有效
        :return:
        """
        return self.get_apply_obj().money

    def get_apply_model(self):
        """
            获取 申请 目标 model
        :return:
        """
        taget = ContentType.objects.get(model=self.apply_type)
        return taget.model_class()

    def get_apply_obj(self):
        """
            获取 申请 目标 obj
        :return:
        """
        model = self.get_apply_model()
        obj = model.objects.get(id=self.apply_type_id)
        return obj

    @classmethod
    def add_apply(cls, **kwargs):
        """
            点击申请
        :return:
        """
        msg = ''
        customer = kwargs.pop("customer")
        target_type = kwargs.get("target_type")
        target_id = kwargs.get("target_id")

        # apply_type = kwargs.get("apply_obj_type")
        # apply_type_id = kwargs.get("apply_obj_type_id")
        # 判断用户身份能否申请
        check = CHECK_APPLY.get(customer.customer_type)
        if target_type not in TARGET_TYPE or check[0] != target_type:
            msg = check[-1]
            return False, msg

        if customer.customer_type == 1:
            apply_type_id = customer.teacher_set.filter(is_valid=True).first().id
            apply_type = 'teacher'
        elif customer.customer_type == 2:
            apply_type_id = customer.student_set.filter(is_valid=True).first().id
            apply_type = 'student'

        if not cls.objects.filter(is_valid=True,
                                  target_type=target_type,
                                  target_id=target_id,
                                  apply_type=apply_type,
                                  apply_type_id=apply_type_id).exists():
            kwargs['apply_customer_id'] = customer.id
            kwargs['apply_type_id'] = apply_type_id
            kwargs['apply_type'] = apply_type
            apply = cls(**kwargs)
            apply.target_customer_id = apply.get_target_obj().customer_id
            apply.save(force_insert=True)
            return apply.id, msg
        msg = '不能重复申请'
        return False, msg

    def delete_apply(self):
        """
            删除
        :return:
        """
        if self.is_valid:
            self.is_valid = False
            self.save()