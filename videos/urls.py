from django.urls import path
from .views import VideoUploadView, VideoListView

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('', VideoListView.as_view(), name='video-list'),
]
