
from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import *

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Work)
class WorkAdmin(SummernoteModelAdmin):
    list_display = ("title", "type", "year")
    list_filter = ("type", "genres")
    search_fields = ("title",)
    summernote_fields = ("description",)


@admin.register(WorkChain)
class WorkChainAdmin(admin.ModelAdmin):
    list_display = ("root", "next", "label")


@admin.register(Character)
class CharacterAdmin(SummernoteModelAdmin):
    list_display = ("full_name", "sex", "work")
    list_filter = ("sex", "work")
    search_fields = ("full_name",)
    summernote_fields = ("bio",)


@admin.register(CharacterImage)
class CharacterImageAdmin(admin.ModelAdmin):
    list_display = ("character", "created_at")


admin.site.register(Skill)
admin.site.register(Trait)
