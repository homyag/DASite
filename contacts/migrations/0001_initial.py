# Generated by Django 5.1.5 on 2025-04-11 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя')),
                ('email', models.EmailField(max_length=254, verbose_name='Email')),
                ('phone', models.CharField(max_length=17, verbose_name='Телефон')),
                ('service', models.CharField(choices=[('web_development', 'Веб-разработка'), ('mobile_development', 'Мобильная разработка'), ('design', 'Дизайн'), ('seo', 'SEO оптимизация'), ('marketing', 'Маркетинг'), ('other', 'Другое')], default='web_development', max_length=50, verbose_name='Услуга')),
                ('message', models.TextField(verbose_name='Сообщение')),
                ('status', models.CharField(choices=[('new', 'Новая'), ('in_progress', 'В обработке'), ('completed', 'Завершена'), ('canceled', 'Отменена')], default='new', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Заявка',
                'verbose_name_plural': 'Заявки',
                'ordering': ['-created_at'],
            },
        ),
    ]
