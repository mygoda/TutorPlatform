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


class City(CommonModel):
    """城市"""

    code = models.CharField(u"城市编码", max_length=32)
    name = models.CharField(u"城市名称", max_length=32)

    def __unicode__(self):
        return self.name


class Subject(CommonModel):
    """科目"""

    name = models.CharField(u"科目", max_length=16)

    def __unicode__(self):
        return self.name


class BaseLevel(CommonModel):
    """小学还是初中"""

    name = models.CharField(u"名称", max_length=16)

    def __unicode__(self):
        return self.name


class Level(CommonModel):
    """年级"""

    base = models.ForeignKey(BaseLevel, verbose_name=u"小/初/高")
    name = models.CharField(u"年级", max_length=12)

    def __unicode__(self):
        return self.name


class School(CommonModel):
    """学校"""

    city = models.ForeignKey(City, verbose_name="城市")
    name = models.CharField(u"学校名称", max_length=64)

    def __unicode__(self):
        return self.name