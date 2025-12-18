from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.templatetags.static import static
from apps.catalog.models.work import *


class WorkChain(models.Model):
    """Связь материалов в единую цепочку (сезоны, тома и т.п.)."""
    root = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="chain_root")
    next = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="chain_next")
    label = models.CharField(max_length=64, blank=True, help_text="Например: Сезон 2 / Том 3")

    class Meta:
        unique_together = ("root", "next")

    def __str__(self):
        return f"{self.root.title} → {self.next.title} ({self.label})"