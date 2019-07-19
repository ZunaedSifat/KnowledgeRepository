from django.db import connection, ProgrammingError
from django.shortcuts import render, redirect

from .forms import DocumentForm
from .models import DocumentModel, KeywordModel
import os
from .ocr import extract_text
from KnowledgeRepository.settings import MEDIA_ROOT
from . import summakeywords
from . import wordart
from django.http import HttpResponse


def sql_select(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    results_list = []
    try:
        results = cursor.fetchall()
    except ProgrammingError as e:
        # print(e)
        return []

    i = 0
    for row in results:
        dict = {}
        field = 0
        while True:
            try:
                dict[cursor.description[field][0]] = str(results[i][field])
                field = field + 1
            except IndexError as e:
                break
        i = i + 1
        results_list.append(dict)
    return results_list


def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            document = DocumentModel.objects.get(pk=obj.pk)
            document_path = document.document
            document.uploader = request.user.pk
            print('pk', request.user)
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


def search(request):
    return render(request, 'documents/search.html')


def search_results(request):
    if request.method == 'POST':
        author = request.POST.get("author")
        title = request.POST.get("title")
        keywords = str(request.POST.get("keywords")).split()
        print(author, title, keywords)

    return render(request, 'documents/search_results.html')
