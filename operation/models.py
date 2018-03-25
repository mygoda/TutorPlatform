# -*- coding: utf-8 -*-
"""
    用户操作 app model
"""

import logging

from django.db import models

from common import models as common_models
from customer import models as customer_models


TARGET_TYPE = ['teacher', 'student']

USER_TYPE = {
    0: '没有注册',
    1: '教师',
    2: '学生'
}

CHECK_FAV = {
    0: ['ours', '您尚未注册'],
    1: ['student', '仅学生才能收藏教师'],
    2: ['teacher', '仅教师才能收藏学生']
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
    customer_type_id = models.IntegerField(default=0, verbose_name=u'用户身份id')

    class Meta:
        verbose_name = u'用户收藏'
        verbose_name_plural = verbose_name

    @property
    def target_name(self):
        """
            收藏对象 name
        :return:
        """
        return self.get_target_obj().name

    @property
    def target_subject(self):
        """
         收藏对象  科目
        :return:
        """
        return [subject.subject.name for subject in self.get_target_obj().studentsubjectsship_set.all()]

    @property
    def target_is_valid(self):
        """
            收藏对象  是否有效
        :return:
        """
        return self.get_target_obj().is_valid

    @classmethod
    def add_favorite(cls, **kwargs):
        """
            点击收藏
        :return:
        """
        msg = ''
        target_type = kwargs.get("target_type")
        customer = kwargs.get("customer")
        target_id = kwargs.get("target_id")
        # 判断用户身份能否收藏
        check = CHECK_FAV.get(customer.customer_type)
        if target_type not in TARGET_TYPE or check[0] != target_type:
            msg = check[-1]
            return False, msg
        if not cls.objects.filter(is_valid=True, target_type=target_type, target_id=target_id, customer=customer).exists():
            kwargs['customer_type'] = USER_TYPE.get(customer.customer_type)
            kwargs['customer_type_id'] = customer.customer_type
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
    customer = models.ForeignKey(customer_models.Customer, null=True, blank=True, verbose_name=u'用户')
    target_id = models.IntegerField(default=0, verbose_name=u'申请对象id')
    target_type = models.CharField(max_length=64, verbose_name=u'申请对象')
    is_valid = models.BooleanField(u"是否有效", default=True)
    customer_type = models.CharField(max_length=64, verbose_name=u'用户收藏时身份')
    customer_type_id = models.IntegerField(verbose_name=u'用户身份id')

    class Meta:
        verbose_name = u'用户申请'
        verbose_name_plural = verbose_name

