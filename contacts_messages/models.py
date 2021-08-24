from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

STATUS = (
    (0, 'Non envoyé'),
    (1, 'En cours d\'envoi'),
    (2, 'Envoyé'),
    (3, 'Erreur')
)

LIST_RECEIVERS = (
    (0, 'Tout le monde'),
    (1, 'Adhérents'),
    (2, 'Non adhérents'),
#    (3, 'Abonnés'),
#    (4, 'Non abonnés')
)


class Message(models.Model):
    subject = models.CharField('sujet', max_length=50)
    body = RichTextUploadingField('corps')
    status = models.IntegerField('statut', choices=STATUS, default=0)
    receivers = models.IntegerField('destinataires', choices=LIST_RECEIVERS, default=0)

    class Meta:
        verbose_name = 'message'
        verbose_name_plural = 'messages'

    def __str__(self):
        return self.subject


class Attachment(models.Model):
    message = models.ForeignKey(Message, default=None, on_delete=models.CASCADE, related_name='attachments')
    attachment = models.FileField('image', upload_to='protected/messages/attachments')

    class Meta:
        verbose_name = 'pièce jointe'
        verbose_name_plural = 'pièces jointes'

    def __str__(self):
        return self.message.subject