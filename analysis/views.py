# analysis/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import AnalysisResult
from .serializers import AnalysisResultSerializer
from videos.models import Video
from django.shortcuts import get_object_or_404

class AnalysisResultView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, video_id):
        video = get_object_or_404(Video, id=video_id, user=request.user)
        result = get_object_or_404(AnalysisResult, video=video)
        serializer = AnalysisResultSerializer(result)
        return Response(serializer.data)
