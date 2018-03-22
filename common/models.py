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

    @property
    def create_time(self):
        return self.created_at.strftime("%Y-%m-%d")


class City(CommonModel):
    """城市"""

    code = models.CharField(u"城市编码", max_length=32)
    name = models.CharField(u"城市名称", max_length=32)

    # def __unicode__(self):
    #     return self.name

    class Meta:
        verbose_name = u'城市'
        verbose_name_plural = verbose_name

class Subject(CommonModel):
    """科目"""

    name = models.CharField(u"科目", max_length=16)
    checked = models.BooleanField(u"是否选中", default=False)

    # def __unicode__(self):
    #     return self.name

    class Meta:
        verbose_name = u'科目'
        verbose_name_plural = verbose_name


class BaseLevel(CommonModel):
    """小学还是初中"""

    name = models.CharField(u"名称", max_length=16)

    # def __unicode__(self):
    #     return self.name

    class Meta:
        verbose_name = u'学校等级'
        verbose_name_plural = verbose_name

    @property
    def level(self):
        return self.level_set.all()


class Level(CommonModel):
    """年级"""

    base = models.ForeignKey(BaseLevel, verbose_name=u"小/初/高")
    name = models.CharField(u"年级", max_length=12)

    # def __unicode__(self):
    #     return self.name

    class Meta:
        verbose_name = u'年级'
        verbose_name_plural = verbose_name


class Basis(CommonModel):
    """学生基础"""

    name = models.CharField(u"学生基础", max_length=12)

    # def __unicode__(self):
    #     return self.name

    class Meta:
        verbose_name = u'学生基础'
        verbose_name_plural = verbose_name


class Learn(CommonModel):
    """学历"""

    name = models.CharField(u"学历", max_length=12)

    # def __unicode__(self):
    #     return self.name

    class Meta:
        verbose_name = u'学历'
        verbose_name_plural = verbose_name


class School(CommonModel):
    """学校"""

    city = models.ForeignKey(City, verbose_name="城市")
    name = models.CharField(u"学校名称", max_length=64)
    level = models.CharField(u"学校等级", default=985, max_length=24)

    # def __unicode__(self):
    #     return self.name

    class Meta:
        verbose_name = u'学校'
        verbose_name_plural = verbose_name


class TeacherType(CommonModel):
    """
        教学 特点 标签
    """

    name = models.CharField(u"特点", max_length=200)
    checked = models.BooleanField(u"是否选中", default=False)

    class Meta:
        verbose_name = u'教师特点'
        verbose_name_plural = verbose_name


class StudentType(CommonModel):
    """
        学生特点 存在的问题 标签
    """

    name = models.CharField(u"存在问题", max_length=200)
    checked = models.BooleanField(u"是否选中", default=False)

    class Meta:
        verbose_name = u'学生存在问题'
        verbose_name_plural = verbose_name


class TeacherRequire(CommonModel):
    """
        教师资质，学生对教师的要求
    """

    name = models.CharField(u"教师资质", max_length=64)

    class Meta:
        verbose_name = u'教师资质'
        verbose_name_plural = verbose_name


class Reason(CommonModel):
    """
        原因
    """
    name = models.CharField(u"原因", max_length=64)

    class Meta:
        verbose_name = u'原因'
        verbose_name_plural = verbose_name