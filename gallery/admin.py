from django.contrib import admin

from .models import Gallery, GalleryImage, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'gallery', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('body',)
    fields = ('gallery', 'body', 'active')
    actions = ['approve_comments']

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
    approve_comments.short_description = 'Approuvé les commentaires sélectionnés'


class GalleryImageInline(admin.StackedInline):
    model = GalleryImage


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_on')
    search_fields = ['title', ]
    prepopulated_fields = {'slug': ('title',)}
    fields = ('title', 'slug', 'description', 'cover')
    inlines = [GalleryImageInline]

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.author = request.user

        super().save_model(request, obj, form, change)
