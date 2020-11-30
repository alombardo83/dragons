from django.db import models
from django.contrib.auth.models import User


class Gallery(models.Model):
    title = models.CharField('titre', max_length=250)
    slug = models.SlugField('slug', max_length=200, unique=True)
    description = models.TextField('description')
    cover = models.FileField('couverture', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='galleries')

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'galerie'
        verbose_name_plural = 'galeries'

    def __str__(self):
        return self.title


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, default=None, on_delete=models.CASCADE)
    image = models.FileField('image', upload_to='images/')

    class Meta:
        verbose_name = 'image'
        verbose_name_plural = 'images'

    def __str__(self):
        return self.gallery.title


class Comment(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gallery_comments')
    body = models.TextField('corps')
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'commentaire'
        verbose_name_plural = 'commentaires'

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author.get_username)