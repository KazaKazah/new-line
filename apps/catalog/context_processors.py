# catalog/context_processors.py
from .models import Work, Genre


def common_nav(request):
    """
    Данные для навбара: список типов и жанров.
    Доступно во всех шаблонах как nav_types и nav_genres.
    """
    return {
        "nav_types": Work.TYPE_CHOICES,
        "nav_genres": Genre.objects.all(),
    }