# Generated by Django 2.2.3 on 2019-07-19 16:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='documents/')),
                ('title', models.CharField(max_length=512)),
                ('author', models.TextField(max_length=128)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('uploader', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='KeywordModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=32)),
                ('document', models.ManyToManyField(to='documents.DocumentModel')),
            ],
        ),
        migrations.CreateModel(
            name='CitationModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cited_by', models.ManyToManyField(related_name='cited_me', to='documents.DocumentModel')),
                ('cited_to', models.ManyToManyField(related_name='i_cited', to='documents.DocumentModel')),
            ],
        ),
    ]