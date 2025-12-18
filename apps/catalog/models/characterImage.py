from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.templatetags.static import static
from apps.catalog.models.character import *


class CharacterImage(models.Model):
    """Изображение или фотография персонажа."""
    character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name="gallery")  #"Персонаж, к которому относится изображение."
    image = models.ImageField(upload_to="character_gallery/")   #"Изображение персонажа."
    caption = models.CharField(max_length=200, blank=True)      #"Подпись или описание изображения."
    created_at = models.DateTimeField(auto_now_add=True)            #"Дата и время добавления изображения."

    class Meta:
        ordering = ["-created_at"]

    def image_url(self):
        try:
            if self.image and self.image.name and self.image.storage.exists(self.image.name):
                return self.image.url
        except Exception:
            pass
        return static("catalog/img/placeholder_character.jpg")

    def __str__(self):
        return f"Фото {self.character.full_name}"