from django.urls import path
from accounts import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


urlpatterns = [
    path('info', views.AccountInfoAPIView.as_view()),
    path('registration', views.RegistrationAPIView.as_view()),
    path('email/confirm/<str:pk>', views.EmailConfirmAPIView.as_view()),
    path('password/reset', views.PasswordResetAPIView.as_view()),
    path('password/reset/confirm/<str:pk>', views.PasswordResetConfirmAPIView.as_view()),
    path("token", TokenObtainPairView.as_view()),
    path("token/refresh", TokenRefreshView.as_view()),
]