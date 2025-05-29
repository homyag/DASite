from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_remove_servicecase'),  # Замените на номер последней миграции
    ]

    operations = [
        migrations.RunSQL(
            # Проверяем и удаляем таблицу если она еще существует
            """
            DO $$ 
            BEGIN
                IF EXISTS (SELECT FROM information_schema.tables 
                          WHERE table_schema = 'public' 
                          AND table_name = 'services_servicecase') THEN
                    DROP TABLE services_servicecase CASCADE;
                END IF;
            END $$;
            """,
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]