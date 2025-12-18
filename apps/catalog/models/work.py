from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.templatetags.static import static
from apps.catalog.models.genre import *


class Work(models.Model):
    'произведения'
    TYPE_CHOICES = [
        ("anime", "Аниме"),
        ("manga", "Манга"),
        ("manhwa", "Манхва"),
        ("manhua", "Маньхуа"),
        ("movie", "Кино"),
        ("series", "Сериал"),
        ("cartoon", "Мультфильм"),
        ("book", "Книга"),
    ]
    type = models.CharField(max_length=16, choices=TYPE_CHOICES)  #'type произведения'    
    title = models.CharField(max_length=200)    #'название'
    slug = models.SlugField(max_length=220, unique=True, blank=True) #'url-имя'
    year = models.PositiveIntegerField(null=True, blank=True) #'год выпуска'
    description = models.TextField(blank=True)#'описание'
    poster = models.ImageField(upload_to="work_posters/", blank=True, null=True) #'постер'
    genres = models.ManyToManyField(Genre, related_name="works", blank=True) #'жанры's

    class Meta:
        ordering = ["title"]
        indexes = [models.Index(fields=["type", "title"])]

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title or "")
            self.slug = base or slugify(f"work-{self.pk or ''}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("work-detail", args=[self.slug])

    def poster_url(self):
        try:
            if self.poster and self.poster.name and self.poster.storage.exists(self.poster.name):
                return self.poster.url
        except Exception:
            pass
        return static("catalog/img/placeholder_work.jpg")

    def __str__(self):
        return f"{self.get_type_display()}: {self.title}"