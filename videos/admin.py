from django.contrib import admin
from .models import Video

class VideoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'uploaded_at', 'is_analyzed')
    list_filter = ('is_analyzed', 'uploaded_at')
    search_fields = ('user__email',)
    ordering = ('-uploaded_at',)

admin.site.register(Video, VideoAdmin)
