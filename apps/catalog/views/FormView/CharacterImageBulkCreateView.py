from apps.catalog.views.layout import *


class CharacterImageBulkCreateView(LoginRequiredMixin, FormView):
    '''View для массовой загрузки изображений персонажа.'''
    form_class = CharacterImagesBulkForm
    template_name = "catalog/character_image_add_multi.html"

    def dispatch(self, request, *args, **kwargs):
        self.character = get_object_or_404(Character, slug=self.kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial["character"] = self.character.pk
        return initial

    def form_valid(self, form):
        files = form.cleaned_data["images_list"]  # из clean()
        caption = form.cleaned_data.get("caption") or ""

        # ВАЖНО: сохраняем по одному, чтобы сработал FileField storage
        for f in files:
            img = CharacterImage(character=self.character, caption=caption)
            img.image = f  # привязываем файл
            img.save()  # только save() реально пишет файл на диск

        return redirect("character-gallery", slug=self.character.slug)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["character"] = self.character
        return ctx


try:
    import rarfile

    HAVE_RAR = True
except Exception:
    HAVE_RAR = False

