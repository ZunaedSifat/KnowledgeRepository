from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('upload/files/', views.upload, name='upload_files'),
    path('add_post/', views.add_post, name='add_post'),
    path('show_post/<int:pk>', views.show_post, name='show_post'),
    path('search/', views.search, name='search'),
    path('search_results/', views.search_results, name='search_results')
]
