# coding=utf-8
"""tutor URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework_swagger.views import get_swagger_view
from rest_framework import routers

from student import views as student_views
from teacher import views as teacher_views


URL_ID = "(?P<id>[0-9]+)"

schema_view = get_swagger_view(title='家教平台接口')
router = routers.DefaultRouter()
router.register(r"students", student_views.StudentViewset, base_name="student_api")
router.register(r"teacher", teacher_views.TeacherViewset, base_name="teacher_api")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^docs/', schema_view),

]
