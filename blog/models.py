from uuid import uuid4
from pathlib import Path
from django.conf import settings
from django.db import models
from django.urls import reverse

def post_image_path(instance, filename):
    return f'posts/{uuid4().hex}{Path(filename).suffix.lower()}'

class Post(models.Model):
    title = models.CharField('Título', max_length=180)
    content = models.TextField('Contenido')
    image = models.ImageField('Imagen', upload_to=post_image_path, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at', '-pk']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'pk': self.pk})
