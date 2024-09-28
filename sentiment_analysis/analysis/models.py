from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Record(models.Model):
    chat_file = models.TextField()
    sentiment_score = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    def __str__(self):
        return f"Record {self.id}"





    #sentiment_score = models.JSONField(null=True, blank=True)
    






#chat_file = models.FileField(upload_to='chats/'
