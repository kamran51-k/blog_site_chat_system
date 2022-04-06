from blogchat_app.models import ContactModel2, LogoModel,NavbarModel
def header_and_footer(request):
    context = {}
    base_queryset = NavbarModel.objects.all()
    logo_queryset = LogoModel.objects.all()
    contact_queryset_two = ContactModel2.objects.all()
    context['logo_queryset'] = logo_queryset
    context['base_queryset'] = base_queryset
    context['contact_queryset_two'] = contact_queryset_two

    return context
