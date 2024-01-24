# Generated by Django 5.0 on 2023-12-24 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('diplom_API', '0003_alter_filedata_external_download_link'),
    ]

    operations = [
        migrations.RenameField(
            model_name='filedata',
            old_name='name',
            new_name='filename',
        ),
        migrations.RenameField(
            model_name='filedata',
            old_name='path',
            new_name='filepath',
        ),
        migrations.RemoveField(
            model_name='filedata',
            name='size',
        ),
        migrations.AddField(
            model_name='filedata',
            name='filesize',
            field=models.PositiveIntegerField(blank=True, editable=False, null=True),
        ),
    ]
