from django.conf import settings
from django.conf.urls import url

from .views import *

urlpatterns = [
    url(r'^$', StandardList.as_view(), name='standard_list'),
    url(r'test/$',SubjectTest.as_view(),name='subject_test')
]