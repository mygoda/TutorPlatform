# coding=utf-8
from django.contrib.contenttypes.models import ContentType
from django.db import models

# Create your models here.


class CommonModel(models.Model):

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

    def get_target_model(self):
        """
            获取 目标 model
        :return:
        """
        taget = ContentType.objects.get(model=self.target_type)
        return taget.model_class()

    def get_target_obj(self):
        """
            获取 目标 obj
        :return:
        """
        model = self.get_target_model()
        obj = model.objects.get(id=self.target_id)
        return obj

    @property
    def model_name(self):
        """
            在 评论等关联表的时候需要使用
        :return:
        """
        return self.__class__.__name__.lower()



