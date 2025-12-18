from apps.catalog.views.layout import *

class WorkDetailView(LoginRequiredMixin, DetailView):
    '''Просмотр детали произведения.'''
    model = Work
    slug_field = "slug"
    template_name = "catalog/work_detail.html"
    context_object_name = "work"

