from django.urls import path
from . import views

urlpatterns = [
    path('info/', views.get_video_info),
    path('download/', views.download_video),
    path('downloaded/<str:filename>/', views.serve_downloaded_file),
]
