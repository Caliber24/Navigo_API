"""
URL configuration for NAVIGO project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)
urlpatterns = [

    path("register/", UserViewSet.as_view({'post': 'register'}), name="user-register"),
    path("users/me/", UserViewSet.as_view({"get": "me", "put": "me", "patch": "me"}), name="user-me"),
    path("resend_activation/", UserViewSet.as_view({"post": "resend_activation"}), name="resend-activation"),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),

    path("activate/<str:email>/", UserViewSet.as_view({"post": "activate"}), name="user-activate"),
    path("reset-password/", UserViewSet.as_view({"post": "send_reset_password_code"}), name="reset-password-code"),
    path("reset-password/code/<str:email>", UserViewSet.as_view({"post": "reset_password_code"}), name="reset-password"),

    path("users/me/avatar/", UserViewSet.as_view({"post": "update_avatar", 'get': 'get_avatar',"delete": "delete_avatar"}), name="user-avatar"),
]