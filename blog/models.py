from django.db import models
from django.contrib.auth.models import User
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils.translation import gettext, gettext_lazy as _

STATUS = (
    (0, _('Draft')),
    (1, _('Publish'))
)

class Post(models.Model):
    title = models.CharField(_('title'), max_length=200, unique=True)
    slug = models.SlugField(_('slug'), max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    updated_on = models.DateTimeField(auto_now=True)
    content = RichTextUploadingField(_('content'), )
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(_('status'), choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']
        permissions = (('can_publish', 'Set a post as published'),)
        verbose_name = _('post')
        verbose_name_plural = _('posts')

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    body = models.TextField(_('body'))
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']
        verbose_name = _('comment')
        verbose_name_plural = _('comments')

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.author.get_username)

