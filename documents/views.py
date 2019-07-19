from django.shortcuts import render, redirect
from .forms import DocumentForm
from .models import Document


def upload(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            document_path = Document.objects.get(pk=obj.pk).document
            print()

            return redirect('homepage')
    else:
        form = DocumentForm()
    return render(request, 'documents/upload.html', {
        'form': form
    })
