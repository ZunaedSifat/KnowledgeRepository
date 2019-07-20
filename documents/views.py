from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .forms import DocumentForm, ForumPostCreationForm
from .models import DocumentModel, KeywordModel, ForumPost
from django.db import connection, ProgrammingError
import os
from .ocr import extract_text
from KnowledgeRepository.settings import MEDIA_ROOT
from . import summakeywords
from . import wordart
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


# returns a list of dictionary
def sql_select(sql):
    print('Query', sql)
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
            except ConnectionAbortedError as ca:
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

            document.ocr_text = text

            keywords = summakeywords.generate_summa_keywords(text, 'temp/keywords.txt')
            print(keywords)
            wordart.generate_word_art('temp/keywords.txt', outputfile='wordart')
            document.word_art = os.path.abspath('wordart.png')
            document.save()

            ts_vec = "UPDATE documents_documentmodel d1 SET ts_vector = to_tsvector(d1.ocr_text)  where id = #doc_id; "
            ts_vec = ts_vec.replace('#doc_id', str(document.pk))
            sql_select(ts_vec)
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

            return HttpResponse('success!')  # todo pass context
    else:
        form = DocumentForm()
        print(form.as_p())
    return render(request, 'documents/upload.html', {
        'form': form
    })


def upload_additional(request):
    # return HttpResponse("<h1>Hello there!!!</h1>")
    return render(request, 'documents/upload_additional.html', {'context': 'wow'})


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


def search(request):
    return render(request, 'documents/search.html')


def find_docs_that_match_keyword(keyword: str):
    doc_ids = sql_select(str(query_get_doc_id).replace('#keyword', keyword))
    results = dict()
    for i in doc_ids:
        # print(i)
        for k, v in i.items():
            if results.get(v) is None:
                results[v] = 1
            else:
                results[v] = results[v] + 1
    print(results)
    return results


def find_docs_that_match_keywords(keywords: list):
    results = dict()
    final_res = dict()

    for k in keywords:
        results = (find_docs_that_match_keyword(k))
        print(results)
        for key, val in results.items():
            print('doc', key)
            if final_res.get(key) is None:
                final_res[key] = 1
            else:
                final_res[key] = final_res[key] + 1

    return final_res  # todo maybe do sort based on values


def remove_duplicates(x: list):
    return list(dict.fromkeys(x))


query_title = "select id from documents_documentmodel where lower(title) like '%#title%';"
query_author = "select id from documents_documentmodel where lower(author) like '%#author%';"

query_title_author = "(select id from documents_documentmodel where lower(author) = '#author' )UNION (select id from " \
                     "documents_documentmodel where lower(title) = '#title' ) "

query_get_doc_id = "select documentmodel_id from documents_keywordmodel_document" \
                   " where  keywordmodel_id = (select id from documents_keywordmodel " \
                   "where text =lower('#keyword'))"

query_text_search = "SELECT id FROM documents_documentmodel WHERE ts_vector @@ to_tsquery(lower('#text'));"


@csrf_exempt
def search_results(request):
    results = list()
    value = str()
    if request.method == 'POST':
        type = request.POST.get("select")
        value = str(request.POST.get("value")).lower()
        if str(type).lower() == 'author':
            results = sql_select(query_author.replace('#author', value))
        elif str(type).lower() == 'title':
            results = sql_select(query_title.replace('#title', value))
        elif str(type).lower() == 'text search':
            results = sql_select(query_text_search.replace('#text', value.replace(' ', '|')))

    print('value', value)
    print('res1', results)
    result_docs = []

    try:
        keywords = request.POST.get("keylist")
        keywords = str(keywords).split(',')
        print('keywords', keywords)
        results2 = find_docs_that_match_keywords(keywords)
        results2 = sorted(results2.items(), key=lambda x: x[1], reverse=True)
        print('res2', results2)
        for item in results2:
            (doc_id, count) = item
            d = DocumentModel.objects.get(int(str(doc_id).strip()))
            result_docs.append(d)
    except ConnectionAbortedError as e:
        print("Why did an error occur?")

    for item in results:
        d = DocumentModel.objects.get(int(item["id"].strip()))
        result_docs.append(d)


    return render(request, 'documents/search.html', context={'context': result_docs})

