from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import DocumentModel, KeywordModel
import os
from .ocr import extract_text
from KnowledgeRepository.settings import MEDIA_ROOT
from . import summakeywords
from . import wordart
from django.http import HttpResponse


def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():

            print("came here")

            obj = form.save()
            document = DocumentModel.objects.get(pk=obj.pk)
            document_path = document.document
            document.uploader = request.user.pk
            document.save()

            full_path = str(os.path.join(MEDIA_ROOT, str(document_path)))
            is_pdf = True if full_path.split(".")[-1].lower() == 'pdf' else False
            text = extract_text(full_path, is_pdf=is_pdf)

            keywords = summakeywords.generate_summa_keywords(text, 'temp/keywords.txt')
            wordart.generate_word_art('temp/keywords.txt', outputfile='wordart')

            context = {
                'keywords': keywords[0:min(10, len(keywords))]
            }

            return
    else:
        form = DocumentForm()
        print(form.as_p())
    return render(request, 'documents/upload.html', {
        'form': form
    })


def add_optional_data(request):
    return HttpResponse("nothing")

