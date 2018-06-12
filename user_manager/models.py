from django.db import models

# Create your models here.

class Notification(models.Model):
    sender = models.CharField(max_length = 50)
    status = models.CharField(max_length = 50)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    message = models.CharField(max_length = 200)

    def __str__(self):
        return self.message