from apps.catalog.views.layout import *


class CharacterGalleryView(LoginRequiredMixin, ListView):
    '''View для галереи изображений персонажа.'''
    template_name = "catalog/character_gallery.html"
    paginate_by = 18
    context_object_name = "images"

    def get_queryset(self):
        character = get_object_or_404(Character, slug=self.kwargs["slug"])
        return CharacterImage.objects.filter(character=character)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["character"] = get_object_or_404(Character, slug=self.kwargs["slug"])
        return ctx
