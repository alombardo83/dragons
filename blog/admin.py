from django.contrib import admin
from django.contrib.auth import get_permission_codename
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings

from core.mail import get_connection
from core.models import Profile
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
            self.fields = ('title', 'slug', 'description', 'content')
        else:
            self.fields = ('title', 'slug', 'description', 'status', 'content')
        return super(PostAdmin, self).get_form(request, obj, **kwargs)

    def has_publish_permission(self, request):
        opts = self.opts
        codename = get_permission_codename('can_publish', opts)
        return request.user.has_perm('%s.%s' % (opts.app_label, codename))

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user

        send_newsletter = (not obj.newsletter_sended) and (obj.status == 1) and ((not obj.pk) or (form.has_changed() and 'status' in form.changed_data))
        super().save_model(request, obj, form, change)
        
        if send_newsletter:
            current_site = get_current_site(request)
            subject = 'Newsletter - ' + obj.title
            
            with get_connection('newsletter') as connection:
                from_email = None
                if hasattr(connection, 'username'):
                    from_email = connection.username
        
                profiles = Profile.objects.filter(signup_confirmation=True, newsletter_subscription=True).all()
                for profile in profiles:
                    message = render_to_string('blog/newsletter.html', {
                        'profile': profile,
                        'protocol': settings.PROTOCOL,
                        'domain': current_site.domain,
                        'post': obj,
                    })
                    profile.user.email_user(subject, '', html_message=message, connection=connection)
            
            obj.newsletter_sended = True
            super().save_model(request, obj, form, change)
