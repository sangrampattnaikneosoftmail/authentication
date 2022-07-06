from django.urls import path
from . import views


urlpatterns = [
    path("signup/", views.SignupCreateAPIView.as_view()),
    path("login/", views.LoginAPIView.as_view()),
    path("me/", views.MeAPIView.as_view()),
    path("login/sessions/", views.UserLoggedinSessionAPIView.as_view()),
    path("logout/", views.UserLogOutSessionAPIView.as_view()),
    path("refresh/<refresh_token>/", views.TokenRefreshAPIView.as_view()),
]