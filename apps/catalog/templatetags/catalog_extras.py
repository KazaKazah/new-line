from django import template

register = template.Library()


# место под дополнительные фильтры/теги

@register.filter
def exists(filefield):
    """
    True, если в БД поле задано и файл реально существует в storage (MEDIA_ROOT и т.п.).
    Безопасно перехватывает ошибки.
    """
    try:
        return bool(filefield and filefield.name and filefield.storage.exists(filefield.name))
    except Exception:
        return False