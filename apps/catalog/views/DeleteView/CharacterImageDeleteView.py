from apps.catalog.views.layout import *

class CharacterImageDeleteView(LoginRequiredMixin, DeleteView):
    '''Удаление изображения персонажа.'''
    model = CharacterImage
    pk_url_kwarg = "pk"
    template_name = "catalog/blank_delete.html"  # не используем, но нужно для DeleteView

    # ограничим удаляемые записи текущим персонажем
    def dispatch(self, request, *args, **kwargs):
        self.character = get_object_or_404(Character, slug=self.kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # удалять можно только фото из галереи этого персонажа
        return CharacterImage.objects.filter(character=self.character)

    def get_success_url(self):
        return reverse_lazy("character-gallery", kwargs={"slug": self.character.slug})