# Generated by Django 5.0 on 2024-01-02 23:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diplom_API', '0008_alter_filedata_filepath'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedata',
            name='external_download_link',
            field=models.UUIDField(blank=True, null=True),
        ),
    ]
