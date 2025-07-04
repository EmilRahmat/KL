# Generated by Django 4.2.16 on 2025-05-14 12:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettings',
            name='background_color',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Цвет фона (например, #00000080 для полупрозрачного)'),
        ),
        migrations.AddField(
            model_name='sitesettings',
            name='use_image',
            field=models.BooleanField(default=True, verbose_name='Использовать изображение как фон'),
        ),
    ]
