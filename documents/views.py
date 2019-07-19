

from django.shortcuts import render, redirect, get_object_or_404
from .forms import DocumentForm, ForumPostCreationForm
from .models import DocumentModel, KeywordModel, ForumPost
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

            full_path = str(os.path.join(MEDIA_ROOT, str(document_path)))
            is_pdf = True if full_path.split(".")[-1].lower() == 'pdf' else False
            text = extract_text(full_path, is_pdf=is_pdf)

            keywords = summakeywords.generate_summa_keywords(text, 'temp/keywords.txt')
            print(keywords)
            wordart.generate_word_art('temp/keywords.txt', outputfile='wordart')
            document.word_art = os.path.abspath('wordart.png')
            document.save()

            context = {
                'keywords': keywords[0:min(10, len(keywords))]
            }

            for word, _ in keywords:
                try:
                    keyword = KeywordModel.objects.get(text=word)
                except Exception as e:
                    keyword = KeywordModel.objects.create(text=word)

                keyword.document.add(document)
                keyword.save()

            return HttpResponse('success!')
    else:
        form = DocumentForm()
        print(form.as_p())
    return render(request, 'documents/upload.html', {
        'form': form
    })


def add_optional_data(request):
    return HttpResponse("nothing")


def add_post(request):
    if request.method == 'POST':
        form = ForumPostCreationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    else:
        form = ForumPostCreationForm()
    return render(request, 'documents/upload.html', {
        'form': form
    })


def show_post(request, pk):
    post = get_object_or_404(ForumPost, pk=pk)
    context = {
        'post': post
    }

    return render(request, 'documents/post.html', context=context)
