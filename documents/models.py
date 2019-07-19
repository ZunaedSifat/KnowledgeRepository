from django.db import models


class Document(models.Model):
    document = models.FileField(upload_to='documents/')
    title = models.CharField(max_length=512)
    uploaded_at = models.DateTimeField(auto_now_add=True)
