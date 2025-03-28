from django.views.generic import TemplateView


class ServicesListView(TemplateView):
    template_name = 'services/list.html'


class ServiceView(TemplateView):
    def get_template_names(self):
        service_name = self.kwargs.get('service_name')
        return [f"services/services_{service_name}.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_name = self.kwargs.get('service_name')

        services_data = [
            {'name': 'seo', 'title': 'SEO-продвижение'},
            {'name': 'email', 'title': 'Email-маркетинг'},
            {'name': 'content', 'title': 'Контент-маркетинг'},
            {'name': 'smm', 'title': 'SMM-продвижение'},
            {'name': 'orm', 'title': 'Репутационный маркетинг'},
            {'name': 'ppc', 'title': 'PPC-реклама'},
        ]

        service_info = next(
            (s for s in services_data if s['name'] == service_name), None)

        context['service_name'] = service_name
        context['service'] = service_info

        return context
