from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.templatetags.static import static


class Genre(models.Model):
    'Жанры'
    name = models.CharField(max_length=64, unique=True)     #'Название жанра'
    slug = models.SlugField(max_length=80, unique=True, blank=True)  #'URL'     

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name