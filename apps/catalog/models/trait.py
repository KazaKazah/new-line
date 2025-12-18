from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.templatetags.static import static


class Trait(models.Model):
    'черты характера'
    name = models.CharField(max_length=80)

    def __str__(self):
        return self.name