from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField

STATUS = (
    (0, 'Brouillon'),
    (1, 'Publié')
)

class Post(models.Model):
    title = models.CharField('titre', max_length=200, unique=True)
    slug = models.SlugField('slug', max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextUploadingField('contenu', )
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField('statut', choices=STATUS, default=0)
    description = models.CharField('description', max_length=200)
    newsletter_sended = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']
        permissions = (('can_publish', 'Publié un article'),)
        verbose_name = 'article'
        verbose_name_plural = 'articles'

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    body = models.TextField('corps')
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'commentaire'
        verbose_name_plural = 'commentaires'

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author.get_username)

