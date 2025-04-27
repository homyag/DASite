from django.core.management.base import BaseCommand
from django.template.loader import get_template
from bs4 import BeautifulSoup
import os
import json
from services.models import Service, ServiceBenefit, ServiceProcess, FAQ, ServiceExplanation

class Command(BaseCommand):
    help = 'Миграция данных услуг из HTML-файлов в базу данных'

    def handle(self, *args, **options):
        # Путь к директории с шаблонами услуг
        templates_dir = 'DASite/templates/services'
        
        # Список файлов для обработки
        service_files = [
            'services_email.html',
            'services_orm.html',
            'services_ppc.html',
            'services_smm.html',
            'services_content.html'
        ]
        
        for file_name in service_files:
            file_path = os.path.join(templates_dir, file_name)
            if not os.path.exists(file_path):
                self.stdout.write(self.style.WARNING(f'Файл {file_path} не найден'))
                continue
                
            try:
                # Загрузка и парсинг HTML
                with open(file_path, 'r', encoding='utf-8') as f:
                    html_content = f.read()
                soup = BeautifulSoup(html_content, 'html.parser')
                
                # Извлечение данных для модели Service
                hero_section = soup.find('section', class_='pt-32 pb-20')
                if not hero_section:
                    self.stdout.write(self.style.WARNING(f'Не найден hero-раздел в файле {file_name}'))
                    continue
                    
                service_name = hero_section.find('h1')
                if not service_name:
                    self.stdout.write(self.style.WARNING(f'Не найден заголовок в файле {file_name}'))
                    continue
                service_name = service_name.text.strip()
                
                service_slug = file_name.replace('services_', '').replace('.html', '')
                
                # Поиск описания
                description = hero_section.find('p', class_='text-xl')
                description_text = description.text.strip() if description else ''
                
                # Поиск подзаголовка объяснения
                explanation_subtitle = soup.find('p', class_='text-xl text-gray-600')
                explanation_subtitle_text = explanation_subtitle.text.strip() if explanation_subtitle else ''
                
                # Создание или обновление услуги
                service, created = Service.objects.get_or_create(
                    slug=service_slug,
                    defaults={
                        'name': service_name,
                        'title': service_name,
                        'description': description_text,
                        'hero_title': service_name,
                        'hero_description': description_text,
                        'explanation_title': f'Что такое {service_name}?',
                        'explanation_subtitle': explanation_subtitle_text,
                        'process_title': 'Как мы работаем',
                        'process_subtitle': explanation_subtitle_text,
                        'is_active': True,
                        'is_featured': True
                    }
                )
                
                # Извлечение преимуществ
                benefits = soup.find_all('div', class_='bg-white p-8 rounded-lg shadow-md')
                for benefit in benefits:
                    title = benefit.find('h3', class_='text-xl font-bold')
                    description = benefit.find('p', class_='text-gray-600')
                    icon = benefit.find('svg')
                    
                    if title and description:
                        ServiceBenefit.objects.get_or_create(
                            service=service,
                            title=title.text.strip(),
                            defaults={
                                'description': description.text.strip(),
                                'icon': str(icon) if icon else '',
                                'order': ServiceBenefit.objects.filter(service=service).count() + 1
                            }
                        )
                
                # Извлечение этапов процесса
                process_steps = soup.find_all('div', class_='bg-white p-6 rounded-lg shadow-md')
                for step in process_steps:
                    title = step.find('h3', class_='text-xl font-bold')
                    description = step.find('p', class_='text-gray-600')
                    
                    if title and description:
                        ServiceProcess.objects.get_or_create(
                            service=service,
                            title=title.text.strip(),
                            defaults={
                                'description': description.text.strip(),
                                'order': ServiceProcess.objects.filter(service=service).count() + 1
                            }
                        )
                
                # Извлечение FAQ
                faq_items = soup.find_all('script', type='application/ld+json')
                for faq in faq_items:
                    try:
                        faq_data = json.loads(faq.string)
                        for item in faq_data.get('mainEntity', []):
                            question = item.get('name', '')
                            answer = item.get('acceptedAnswer', {}).get('text', '')
                            
                            if question and answer:
                                FAQ.objects.get_or_create(
                                    service=service,
                                    question=question,
                                    defaults={
                                        'answer': answer,
                                        'order': FAQ.objects.filter(service=service).count() + 1
                                    }
                                )
                    except json.JSONDecodeError:
                        self.stdout.write(self.style.WARNING(f'Ошибка парсинга JSON в FAQ для файла {file_name}'))
                        continue
                
                self.stdout.write(self.style.SUCCESS(f'Успешно обработан файл {file_name}'))
                
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Ошибка при обработке файла {file_name}: {str(e)}'))
                continue 