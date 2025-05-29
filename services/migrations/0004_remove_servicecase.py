# Generated manually for removing ServiceCase model
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_alter_faq_answer_alter_service_full_description'),
    ]

    operations = [
        # Удаляем модель ServiceCase
        migrations.DeleteModel(
            name='ServiceCase',
        ),
    ]