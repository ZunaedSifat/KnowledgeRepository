from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVectorField


class DocumentModel(models.Model):
    document = models.FileField(upload_to='documents/', null=False)
    title = models.CharField(max_length=512, null=False)
    author = models.TextField(max_length=128, null=False)
    uploader = models.IntegerField(default=1)  # todo: set current user as author
    uploaded_at = models.DateTimeField(auto_now_add=True)
    ts_vector = SearchVectorField(null=True)
    word_art = models.ImageField(null=True)


class KeywordModel(models.Model):
    document = models.ManyToManyField(DocumentModel)
    text = models.CharField(max_length=32)


class CitationModel(models.Model):
    cited_by = models.ManyToManyField(DocumentModel, related_name='cited_me')
    cited_to = models.ManyToManyField(DocumentModel, related_name='i_cited')
