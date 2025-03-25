def services_context(request):
    services = [
        {'name': 'seo', 'title': 'SEO-продвижение'},
        {'name': 'email', 'title': 'Email-маркетинг'},
        {'name': 'content', 'title': 'Контент-маркетинг'},
        {'name': 'smm', 'title': 'SMM-продвижение'},
        {'name': 'orm', 'title': 'Репутационный маркетинг'},
        {'name': 'ppc', 'title': 'PPC-реклама'},
    ]
    return {'services': services}