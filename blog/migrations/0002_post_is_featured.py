# Generated by Django 5.1.5 on 2025-04-01 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_featured',
            field=models.BooleanField(default=False, verbose_name='Отображать на главной'),
        ),
    ]
