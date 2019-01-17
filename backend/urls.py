from django.conf.urls import url, include
from backend import views
from rest_framework import routers
from knox.views import LogoutView, LogoutAllView


router = routers.DefaultRouter()
router.register('posts', views.PostViewSet, 'posts')

urlpatterns = [
    url("^auth/register/$", views.RegistrationAPI.as_view()),
    url("^auth/login/$", views.LoginAPI.as_view()),
    url("^auth/user/$", views.UserAPI.as_view()),
    url("^auth/logout/$", LogoutView.as_view(), name='knox_logout'),
    url("^auth/logoutall/$", LogoutAllView.as_view(), name='knox_logoutall'),
    url("^post/create/$", views.CreatePostAPI.as_view()),
    url('test/', views.NewsbotList.as_view()),
    url('tech/', views.TechpostList.as_view()),
    url('sports/', views.SportspostList.as_view()),
    url('politics/', views.PoliticspostList.as_view()),
]

urlpatterns += router.urls