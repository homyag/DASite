from django.core.management.base import BaseCommand
from django.utils.text import slugify
from cases.models import Case
from core.models import Category
from services.models import Service
from django.db import transaction, connection
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Миграция данных из ServiceCase в приложение Cases'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Показать, что будет сделано, без фактического выполнения миграции',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        if dry_run:
            self.stdout.write(self.style.WARNING('РЕЖИМ ПРЕДВАРИТЕЛЬНОГО ПРОСМОТРА - изменения не будут сохранены'))

        # Получаем данные ServiceCase напрямую из базы данных
        with connection.cursor() as cursor:
            # Проверяем, существует ли таблица services_servicecase
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = 'services_servicecase'
                );
            """)

            table_exists = cursor.fetchone()[0]

            if not table_exists:
                self.stdout.write(self.style.SUCCESS('Таблица services_servicecase не найдена. Миграция не требуется.'))
                return

            # Получаем все записи ServiceCase с информацией о связанных службах
            cursor.execute("""
                SELECT 
                    sc.id,
                    sc.title,
                    sc.description,
                    sc.result,
                    sc.category,
                    sc.image,
                    sc.service_id,
                    s.name as service_name,
                    s.slug as service_slug
                FROM services_servicecase sc
                LEFT JOIN services_service s ON sc.service_id = s.id
            """)

            service_cases = cursor.fetchall()

        if not service_cases:
            self.stdout.write(self.style.SUCCESS('Нет данных ServiceCase для миграции'))
            return

        self.stdout.write(f'Найдено {len(service_cases)} записей ServiceCase для миграции')

        # Создаем или получаем категории на основе существующих в ServiceCase
        categories_map = {}

        with transaction.atomic():
            if not dry_run:
                # Создаем категории для каждого уникального значения category в ServiceCase
                unique_categories = set()
                for row in service_cases:
                    if row[4]:  # category field
                        unique_categories.add(row[4])

                for cat_name in unique_categories:
                    if cat_name:  # Проверяем, что категория не пустая
                        category, created = Category.objects.get_or_create(
                            slug=slugify(cat_name),
                            defaults={
                                'name': cat_name,
                                'description': f'Категория кейсов: {cat_name}'
                            }
                        )
                        categories_map[cat_name] = category

                        if created:
                            self.stdout.write(f'Создана категория: {cat_name}')
                        else:
                            self.stdout.write(f'Найдена существующая категория: {cat_name}')

            # Мигрируем данные
            migrated_count = 0
            errors_count = 0

            for row in service_cases:
                sc_id, title, description, result, category, image, service_id, service_name, service_slug = row

                try:
                    if dry_run:
                        self.stdout.write(f'[ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР] Будет создан кейс: {title}')
                        self.stdout.write(f'  - Сервис: {service_name}')
                        self.stdout.write(f'  - Категория: {category}')
                        self.stdout.write(f'  - Результат: {result}')
                        migrated_count += 1
                        continue

                    # Создаем slug для кейса
                    base_slug = slugify(title)
                    slug = base_slug
                    counter = 1

                    # Проверяем уникальность slug
                    while Case.objects.filter(slug=slug).exists():
                        slug = f"{base_slug}-{counter}"
                        counter += 1

                    # Создаем кейс
                    case = Case.objects.create(
                        title=title,
                        slug=slug,
                        short_description=description[:500] if description else '',  # Ограничиваем длину
                        client=f"Клиент {service_name}" if service_name else "Клиент",  # Генерируем имя клиента
                        content=f"<h2>Описание проекта</h2><p>{description or ''}</p><h2>Результат</h2><p>{result or ''}</p>",
                        result=result or '',
                        featured_image=image if image else None,
                        is_published=True,
                        is_featured=True,
                        meta_title=f"{title} - Кейс {service_name}" if service_name else title,
                        meta_description=(description[:160] if description and len(
                            description) > 160 else description) or ''
                    )

                    # Добавляем категорию, если она есть
                    if category and category in categories_map:
                        case.categories.add(categories_map[category])

                    # Связываем с сервисом через services field
                    if service_id:
                        try:
                            service = Service.objects.get(id=service_id)
                            case.services.add(service)
                        except Service.DoesNotExist:
                            self.stdout.write(
                                self.style.WARNING(f'Сервис с ID {service_id} не найден для кейса "{title}"')
                            )

                    self.stdout.write(f'Создан кейс: {case.title} (slug: {case.slug})')
                    migrated_count += 1

                except Exception as e:
                    logger.error(f'Ошибка при миграции ServiceCase {sc_id}: {str(e)}')
                    self.stdout.write(
                        self.style.ERROR(f'Ошибка при миграции "{title}": {str(e)}')
                    )
                    errors_count += 1

            if dry_run:
                self.stdout.write(
                    self.style.SUCCESS(f'ПРЕДВАРИТЕЛЬНЫЙ ПРОСМОТР: будет мигрировано {migrated_count} кейсов')
                )
            else:
                self.stdout.write(
                    self.style.SUCCESS(f'Успешно мигрировано {migrated_count} кейсов')
                )

                if errors_count > 0:
                    self.stdout.write(
                        self.style.WARNING(f'Ошибок при миграции: {errors_count}')
                    )

                self.stdout.write(
                    self.style.SUCCESS('Миграция завершена.')
                )

                # Предлагаем удалить таблицу ServiceCase
                self.stdout.write(
                    self.style.WARNING(
                        'ВНИМАНИЕ: После проверки результатов миграции вы можете удалить таблицу services_servicecase')
                )
                self.stdout.write('Для удаления таблицы выполните:')
                self.stdout.write('python manage.py dbshell')
                self.stdout.write('DROP TABLE services_servicecase CASCADE;')