from django.conf.urls import url, include
from backend import views
from rest_framework import routers


router = routers.DefaultRouter()
router.register('posts', views.PostViewSet, 'posts')

urlpatterns = [
    url("^auth/register/$", views.RegistrationAPI.as_view()),
    url("^auth/login/$", views.LoginAPI.as_view()),
    url("^auth/user/$", views.UserAPI.as_view()),
    url('test/', views.NewsbotList.as_view()),
    url('tech/', views.TechpostList.as_view()),
    url('sports/', views.SportspostList.as_view()),
    url('politics/', views.PoliticspostList.as_view()),
]

urlpatterns += router.urls