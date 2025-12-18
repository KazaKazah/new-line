from apps.catalog.views.layout import *


class WorkListView(LoginRequiredMixin, ListView):
    '''View для списка произведений по типу.'''
    template_name = "catalog/work_list.html"
    context_object_name = "works"
    paginate_by = 9

    def get_queryset(self):
        wtype = self.kwargs["wtype"]
        return Work.objects.filter(type=wtype).prefetch_related("genres")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["wtype"] = self.kwargs["wtype"]
        ctx["genres"] = Genre.objects.all()
        return ctx