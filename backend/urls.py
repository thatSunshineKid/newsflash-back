from django.conf.urls import url, include
from backend import views

urlpatterns = [
    url('test/', views.NewsbotList.as_view()),
]