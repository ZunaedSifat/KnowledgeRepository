from django import forms
from .models import DocumentModel, CitationModel, KeywordModel
=======
from .models import DocumentModel, ForumPost


class DocumentForm(forms.ModelForm):
    class Meta:
        model = DocumentModel
        fields = ('document', 'title', 'author')


class CitationForm(forms.ModelForm):
    class Meta:
        model = CitationModel
        fields = ('cited_to', )


class KeywordForm(forms.ModelForm):
    class Meta:
        model = KeywordModel
        fields = ('text', )
class ForumPostCreationForm(forms.ModelForm):
    class Meta:
        model = ForumPost
        fields = ('title', 'content')
