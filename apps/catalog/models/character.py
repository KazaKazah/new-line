from apps.catalog.models.skill import *
from apps.catalog.models.trait import *
from apps.catalog.models.work import *


class Character(models.Model):
    """Персонаж в произведении."""
    SEX_CHOICES = [("male", "Мужской"), ("female", "Женский")]

    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="characters") #"Основное произведение персонажа."
    appearances = models.ManyToManyField(Work, related_name="appearances", blank=True) #"Произведения, в которых персонаж появляется."

    sex = models.CharField(max_length=6, choices=SEX_CHOICES) #"Пол персонажа."
    full_name = models.CharField(max_length=200) #"Полное имя персонажа."
    slug = models.SlugField(max_length=220, unique=True, blank=True) #"Уникальный слаг для URL персонажа."
    bio = models.TextField(blank=True) #"Биография или описание персонажа."

    poster = models.ImageField(upload_to="character_posters/", blank=True, null=True) #"Постер или изображение персонажа."

    # Общие поля
    height_cm = models.PositiveIntegerField(null=True, blank=True) #"Рост персонажа в сантиметрах."
    weight_kg = models.PositiveIntegerField(null=True, blank=True)  #"Вес персонажа в килограммах."
    age = models.PositiveIntegerField(null=True, blank=True)    #"Возраст персонажа."
    race = models.CharField(max_length=80, blank=True)  #"Раса или вид персонажа."

    # Женские поля
    bust_cm = models.PositiveIntegerField(null=True, blank=True)    #"Обхват груди персонажа в сантиметрах."
    hips_cm = models.PositiveIntegerField(null=True, blank=True)    #"Обхват бёдер персонажа в сантиметрах."
    waist_cm = models.PositiveIntegerField(null=True, blank=True)   #"Обхват талии персонажа в сантиметрах."

    skills = models.ManyToManyField(Skill, blank=True)  #"Навыки и умения персонажа."
    traits = models.ManyToManyField(Trait, blank=True)  #"Черты характера персонажа."

    class Meta:
        ordering = ["full_name"]

    def save(self, *args, **kwargs):    
        if not self.slug:
            base = slugify(self.full_name or "") or "character"
            slug = base
            i = 1
            while Character.objects.exclude(pk=self.pk).filter(slug=slug).exists():
                i += 1
                slug = f"{base}-{i}"
            self.slug = slug
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("character-detail", args=[self.slug])

    def poster_url(self):
        """Вернёт URL реального постера, либо плейсхолдер."""
        try:
            if self.poster and self.poster.name and self.poster.storage.exists(self.poster.name):
                return self.poster.url
        except Exception:
            pass
        return static("catalog/img/placeholder_character.jpg")

    def __str__(self):
        return self.full_name