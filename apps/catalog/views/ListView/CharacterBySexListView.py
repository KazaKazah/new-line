from apps.catalog.views.layout import *


class CharacterBySexListView(LoginRequiredMixin, ListView):
    '''View для списка персонажей по полу в рамках произведения.'''
    template_name = "catalog/character_list.html"
    context_object_name = "characters"
    paginate_by = 9

    def get_queryset(self):
        work = get_object_or_404(Work, slug=self.kwargs["slug"])
        sex = self.kwargs["sex"]
        return Character.objects.filter(work=work, sex=sex)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["work"] = get_object_or_404(Work, slug=self.kwargs["slug"])
        ctx["sex"] = self.kwargs["sex"]
        return ctx