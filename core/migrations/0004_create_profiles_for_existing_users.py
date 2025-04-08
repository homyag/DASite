from django.db import migrations


def create_profiles_for_existing_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Profile = apps.get_model('core', 'Profile')

    for user in User.objects.all():
        Profile.objects.get_or_create(user=user)


def reverse_profiles_creation(apps, schema_editor):
    # Обратная миграция не удаляет профили
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('core', '0003_expertise_profile'),
        # Замените на ID предыдущей миграции с созданием модели Profile
    ]

    operations = [
        migrations.RunPython(create_profiles_for_existing_users,
                             reverse_profiles_creation),
    ]