from django.conf.urls import url, include
from backend import views

urlpatterns = [
    url('test/', views.NewsbotList.as_view()),
    url('tech/', views.TechpostList.as_view()),
    url('sports/', views.SportspostList.as_view()),
    url('politics/', views.PoliticspostList.as_view()),
]