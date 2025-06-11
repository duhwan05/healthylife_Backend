from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Video
from .serializers import VideoUploadSerializer
from rest_framework.generics import ListAPIView
from .serializers import VideoUploadSerializer
# 영상 업로드
class VideoUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        serializer = VideoUploadSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            response_data = serializer.save()
            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 영상 리스트 조회 (자신의 것만)
class VideoListView(ListAPIView):
    serializer_class = VideoUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Video.objects.filter(user=self.request.user).order_by('-uploaded_at')
