from django.contrib import admin

from .models import Message, Attachment


class AttachmentInline(admin.StackedInline):
    model = Attachment
    extra = 0


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'status',)
    inlines = [AttachmentInline]
    fields = ('subject', 'receivers', 'body',)

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['subject', 'receivers', 'body']
        else:
            return []
