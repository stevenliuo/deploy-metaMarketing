from django.urls import path
from ppt_projects import views

urlpatterns = [
    path('projects/', views.ProjectListAPIView.as_view()),
    path('projects/create/', views.ProjectCreateAPIView.as_view()),
    path('projects/<int:pk>/', views.ProjectUpdateAPIView.as_view()),
    path('projects/<int:pk>/generate/', views.ProjectUpdateAPIView.as_view()),
    path('projects/<int:id>/screenshots/', views.ProjectScreenshotsView.as_view()),
    path('projects/<int:pk>/download-ppt/', views.ProjectPPTDownloadView.as_view()),
    path('projects/<int:pk>/delete/', views.ProjectDeleteAPIView.as_view()),
    path('projects/<int:pk>/generate-ppt/', views.GenerateProjectPPTView.as_view()),

    path('projects/<int:pk>/input-workbooks/', views.InputWorkbookListCreateView.as_view()),

    path('slide-instructions/', views.SlideInstructionsCreateView.as_view()),
    path('slide-instructions/<int:id>/', views.SlideInstructionsDetailView.as_view()),

    path('input-workbooks/<int:id>/', views.InputWorkbookDetailView.as_view()),

    path('slide-instructions/<int:pk>/delete/', views.SlideInstructionDeleteAPIView.as_view()),
]
