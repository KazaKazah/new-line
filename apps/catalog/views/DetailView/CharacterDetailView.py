from apps.catalog.views.layout import *


class CharacterDetailView(LoginRequiredMixin, DetailView):
    '''Просмотр детали персонажа.'''
    model = Character
    slug_field = "slug"
    template_name = "catalog/character_detail.html"
    context_object_name = "character"