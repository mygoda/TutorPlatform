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

from common import views as common_views
from customer import views as customer_views
from student import views as student_views
from teacher import views as teacher_views


URL_ID = "(?P<id>[0-9]+)"

schema_view = get_swagger_view(title='家教平台接口')
router = routers.DefaultRouter()
# common api
router.register(r"city", common_views.CityViewset, base_name="city_api")
router.register(r"subject", common_views.SubjectViewset, base_name="subject_api")
router.register(r"baselevel", common_views.BaseLevelViewset, base_name="baselevel_api")
router.register(r"level", common_views.LevelViewset, base_name="level_api")
router.register(r"basis", common_views.BasisViewset, base_name="basis_api")
router.register(r"learn", common_views.LearnViewset, base_name="learn_api")
router.register(r"school", common_views.SchoolViewset, base_name="school_api")
router.register(r"teacher_type", common_views.TeacherTypeViewset, base_name="teacher_type_api")
router.register(r"student_type", common_views.StudentTypeViewset, base_name="student_type_api")
# customer api
router.register(r"customer", customer_views.CustomerViewset, base_name="customer_api")
# student api
router.register(r"students", student_views.StudentViewset, base_name="student_api")
router.register(r"follower/student", student_views.StudentFollowerViewset, base_name="follower_student_api")
router.register(r"follower/teacher", teacher_views.TeacherFollowerViewset, base_name="follower_teacher_api")
# teacher api
router.register(r"teacher", teacher_views.TeacherViewset, base_name="teacher_api")


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/upload/', common_views.upload_file),
    url(r'^docs/', schema_view),

]
