from apps.catalog.views.layout import *


class GenreWorksView(LoginRequiredMixin, ListView):
    '''View для списка произведений по жанру.'''
    template_name = "catalog/work_list.html"
    context_object_name = "works"
    paginate_by = 9

    def get_queryset(self):
        genre = get_object_or_404(Genre, slug=self.kwargs["slug"])
        return genre.works.all().select_related().prefetch_related("genres")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["genre_filter"] = get_object_or_404(Genre, slug=self.kwargs["slug"])
        return ctx