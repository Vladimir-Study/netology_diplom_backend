# Generated by Django 5.0 on 2024-01-02 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diplom_API', '0007_alter_filedata_filepath'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filedata',
            name='filepath',
            field=models.FileField(blank=True, null=True, upload_to='uploads/'),
        ),
    ]
