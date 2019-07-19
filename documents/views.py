from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document
import os
from .ocr import extract_text
from KnowledgeRepository.settings import MEDIA_ROOT


def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            document_path = Document.objects.get(pk=obj.pk).document
            full_path = str(os.path.join(MEDIA_ROOT, str(document_path)))
            # todo : add doc to pdf here

            is_pdf = True if full_path.split(".")[-1].lower() == 'pdf' else False
            print(extract_text(full_path, is_pdf=is_pdf))

            return redirect('homepage')
    else:
        form = DocumentForm()
    return render(request, 'documents/upload.html', {
        'form': form
    })
