from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from services.models import (
    Service, ServiceFeature, ServiceBenefit, ServiceProcess, FAQ,
    ServiceExplanation, ServiceDetail, ServiceCase, ServicePricing, ServicePartner
)

# class ServicesListView(TemplateView):
#     template_name = 'services/list.html'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['services'] = Service.objects.filter(is_active=True).order_by(
#             'order')
#         return context
class ServicesListView(TemplateView):
    template_name = 'services/list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['services'] = Service.objects.filter(is_active=True).order_by('order')
        return context


# class ServiceView(TemplateView):
#     def get_template_names(self):
#         service_name = self.kwargs.get('service_name')
#         return [f"services/services_{service_name}.html"]
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         service_name = self.kwargs.get('service_name')
#
#         # Получаем информацию об услуге из базы данных
#         service = get_object_or_404(Service, name=service_name, is_active=True)
#
#         # Получаем связанные данные
#         features = service.features.all().order_by('order')
#         benefits = service.benefits.all().order_by('order')
#         processes = service.processes.all().order_by('order')
#
#         # Получаем кейсы, связанные с этой услугой
#         related_cases = Case.objects.filter(
#             services=service,
#             is_published=True
#         ).order_by('-created_at')[:3]
#
#         # Добавляем все данные в контекст
#         context['service_name'] = service_name
#         context['service'] = service
#         context['features'] = features
#         context['benefits'] = benefits
#         context['processes'] = processes
#         context['cases'] = related_cases
#
#         # Получаем FAQs для услуги и общие FAQs
#         faqs = list(service.faqs.filter(is_common=False).order_by('order'))
#         common_faqs = list(
#             service.faqs.filter(is_common=True).order_by('order'))
#         context['faqs'] = faqs + common_faqs
#
#         return context

class ServiceView(TemplateView):
    def get_template_names(self):
        # Проверяем, существует ли специальный шаблон для этой услуги
        service_name = self.kwargs.get('service_name')
        specific_template = f"services/services_{service_name}.html"

        # Возвращаем как специальный шаблон, так и общий шаблон
        # Django попробует использовать первый найденный шаблон
        # return [specific_template, "services/service_detail.html"]
        # return [specific_template]
        return ["services/service_detail.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_name = self.kwargs.get('service_name')

        # Получаем информацию об услуге из базы данных
        service = get_object_or_404(Service, name=service_name, is_active=True)

        # Получаем связанные данные
        features = service.features.all().order_by('order')
        benefits = service.benefits.all().order_by('order')
        processes = service.processes.all().order_by('order')

        # Получаем данные из новых моделей
        explanations = service.explanations.all().order_by('order')
        details = service.details.all().prefetch_related('items').order_by('order')
        cases = service.cases.all().order_by('order')
        pricing_plans = service.pricing.all().prefetch_related('features').order_by('order')
        partners = service.partners.all().order_by('order')

        # Получаем FAQs для услуги и общие FAQs
        faqs = list(service.faqs.filter(is_common=False).order_by('order'))
        common_faqs = list(service.faqs.filter(is_common=True).order_by('order'))

        # Добавляем все данные в контекст
        context.update({
            'service_name': service_name,
            'service': service,
            'features': features,
            'benefits': benefits,
            'processes': processes,
            'explanations': explanations,
            'details': details,
            'cases': cases,
            'pricing_plans': pricing_plans,
            'partners': partners,
            'faqs': faqs + common_faqs
        })

        return context