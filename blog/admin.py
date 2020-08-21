from django.contrib import admin
from django.contrib.auth import get_permission_codename
from .models import Post, Comment

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('body',)
    fields = ('post', 'body', 'active')
    actions = ['approve_comments']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = 'Approuvé les commentaires sélectionnés'

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'status', 'created_on', 'author')
    list_filter = ('status',)
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    actions = ['make_published']
    
    def get_form(self, request, obj=None, **kwargs):
        if not self.has_publish_permission(request):
            self.fields = ('title', 'slug', 'content')
        else:
            self.fields = ('title', 'slug', 'status', 'content')
        return super(PostAdmin, self).get_form(request, obj, **kwargs)

    def has_publish_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('can_publish', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)
