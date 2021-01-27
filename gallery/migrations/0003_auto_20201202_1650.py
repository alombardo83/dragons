# Generated by Django 3.1.3 on 2020-12-02 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallery',
            name='cover',
            field=models.FileField(upload_to='public/gallery/covers', verbose_name='couverture'),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='gallery',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='gallery.gallery'),
        ),
        migrations.AlterField(
            model_name='galleryimage',
            name='image',
            field=models.FileField(upload_to='public/gallery/images', verbose_name='image'),
        ),
    ]