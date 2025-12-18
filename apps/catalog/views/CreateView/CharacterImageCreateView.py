from apps.catalog.views.layout import *

class CharacterImageCreateView(LoginRequiredMixin, CreateView):
    '''Создание нового изображения персонажа.'''
    model = CharacterImage
    form_class = CharacterImageForm
    template_name = "catalog/character_image_add.html"  # сделаем легкий шаблон

    def dispatch(self, request, *args, **kwargs):
        self.character = get_object_or_404(Character, slug=self.kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # прячем поле и фиксируем персонажа
        form.bind_character(self.character)
        return form

    def form_valid(self, form):
        form.instance.character = self.character
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("character-gallery", kwargs={"slug": self.character.slug})