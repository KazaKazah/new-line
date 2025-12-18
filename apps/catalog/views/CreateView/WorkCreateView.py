from apps.catalog.views.layout import *

class WorkCreateView(LoginRequiredMixin, CreateView):
    '''Создание нового произведения.'''
    model = Work
    form_class = WorkForm
    template_name = "catalog/form.html"