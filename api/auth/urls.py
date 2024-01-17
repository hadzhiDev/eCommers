from django.urls import path, include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('profile', views.ProfileViewSet)


urlpatterns = [
    path('login/', views.LoginGenericAPIView.as_view()),
    path('register/', views.RegisterGenericApiView.as_view()),
    path('change-password/', views.ChangePasswordApiView.as_view()),
    path('send-reset-password-key/', views.SendResetPasswordKeyApiView.as_view()),
    path('reset-password/', views.ResetPasswordApiView.as_view()),
    path('', include(router.urls))
]