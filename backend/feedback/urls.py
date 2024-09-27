from django.urls import path
from feedback import views

urlpatterns = [
    path('', views.CreateFeedbackView.as_view()),
]
