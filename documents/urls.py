from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('upload/additional/', views.upload_additional, name='upload_additional'),
    path('search/', views.search, name='search'),
]
