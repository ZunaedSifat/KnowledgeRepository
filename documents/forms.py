from django import forms
from .models import DocumentModel, ForumPost


class DocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentModel
        fields = ('document', 'title', 'author')


class ForumPostCreationForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ('title', 'content')
