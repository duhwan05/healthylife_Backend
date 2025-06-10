from django.urls import path
from .views import AnalysisResultView

urlpatterns = [
    path('<int:video_id>/result/', AnalysisResultView.as_view(), name='analysis-result'),
]
