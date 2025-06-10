# analysis/serializers.py
from rest_framework import serializers
from .models import AnalysisResult

class AnalysisResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnalysisResult
        fields = ['score', 'feedback', 'skeleton_image', 'analyzed_at']
