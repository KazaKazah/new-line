from apps.catalog.views.layout import *

class GenreIndexView(LoginRequiredMixin, FormMixin, ListView):
    """
    Страница жанров:
    - GET: показывает форму создания + сетку жанров
    - POST: создаёт жанр и возвращает на себя
    """
    model = Genre
    template_name = "catalog/genre_index.html"
    context_object_name = "genres"
    form_class = GenreForm
    success_url = reverse_lazy("genre-index")
    paginate_by = 0  # без пагинации

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            form.save()
            return redirect(self.get_success_url())
        # если ошибка — показать те же жанры + форму с ошибкой
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["types"] = Work.TYPE_CHOICES  # пригодится в шаблоне/меню
        ctx["form"] = ctx.get("form") or self.get_form()
        return ctx