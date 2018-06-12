from django.contrib import admin
from .models import Notification

# Register your models here.

class NotificationAdmin(admin.ModelAdmin):
    # sender = models.CharField(max_length = 50)
    # status = models.CharField(max_length = 50)
    list_display = ['sender', 'status', 'timestamp', 'message']
    list_filter = ['timestamp']
    search_fields = ['sender', 'status']
    # class Meta:
    #     model = Notification

admin.site.register(Notification, NotificationAdmin)