from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import os
from .ocr import extract_text
from KnowledgeRepository.settings import MEDIA_ROOT
from . import summakeywords
from . import wordart


def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            document_path = Document.objects.get(pk=obj.pk).document
            full_path = str(os.path.join(MEDIA_ROOT, str(document_path)))
            # todo : add doc to pdf here

            is_pdf = True if full_path.split(".")[-1].lower() == 'pdf' else False
            text = extract_text(full_path, is_pdf=is_pdf)
            keywords = summakeywords.generate_summa_keywords(text, 'temp/keywords.txt')
            wordart.generate_word_art('temp/keywords.txt', outputfile='wordart')

            # todo: store keyword in the database

            return redirect('homepage')
    else:
        form = DocumentForm()
        print(form.as_p())
    return render(request, 'documents/upload.html', {
        'form': form
    })
