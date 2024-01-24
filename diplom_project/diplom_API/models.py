from django.db import models
from django.contrib.auth.models import User
from django_currentuser.middleware import get_current_authenticated_user
from diplom_project.settings import BASE_MEDIA_DIR

def user_directory_path(instance, filename):
    return '{0}/{1}/{2}'.format(BASE_MEDIA_DIR, instance.user.username, filename)

class FileData(models.Model):
    filename = models.CharField(max_length=255)
    filesize = models.PositiveIntegerField(editable=False, null=True, blank=True)
    load_date = models.DateTimeField(auto_now_add=True) 
    last_download_date = models.DateTimeField(null=True, blank=True)
    comment = models.TextField(max_length=500, null=True, blank=True)
    filepath = models.FileField(upload_to=user_directory_path, null=True, blank=True)
    external_download_link = models.UUIDField(null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.filesize = self.filepath.size
        super(FileData, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.filename