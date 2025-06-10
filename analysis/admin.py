from django.contrib import admin
from .models import AnalysisResult, PosePoint

class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'score', 'analyzed_at')
    list_filter = ('analyzed_at',)
    search_fields = ('video__user__email',)
    ordering = ('-analyzed_at',)

class PosePointAdmin(admin.ModelAdmin):
    list_display = ('id', 'video', 'frame_number')
    search_fields = ('video__user__email',)
    ordering = ('video', 'frame_number')

admin.site.register(AnalysisResult, AnalysisResultAdmin)
admin.site.register(PosePoint, PosePointAdmin)
