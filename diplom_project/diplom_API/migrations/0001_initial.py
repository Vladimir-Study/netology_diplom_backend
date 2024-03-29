# Generated by Django 5.0 on 2023-12-24 16:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FileData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('size', models.IntegerField()),
                ('load_date', models.DateTimeField(auto_now_add=True)),
                ('last_download_date', models.DateTimeField(blank=True, null=True)),
                ('comment', models.TextField(blank=True, max_length=500, null=True)),
                ('path', models.TextField(max_length=255)),
                ('external_download_link', models.TextField(max_length=255)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]
