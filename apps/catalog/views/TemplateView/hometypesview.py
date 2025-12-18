# --- ИМПОРТЫ ВВЕРХУ ФАЙЛА ---
import io
import os
from pathlib import PurePosixPath
from zipfile import ZipFile, BadZipFile
from django.core.files.base import ContentFile
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView, CreateView, DeleteView, UpdateView
from django.views.generic.edit import FormMixin, FormView
from django.urls import reverse_lazy
from PIL import Image, UnidentifiedImageError
from apps.catalog.models import Work, Genre, Character, CharacterImage
from apps.catalog.forms import WorkForm, CharacterForm, GenreForm, CharacterImageForm, CharacterImagesBulkForm, \
    CharacterImagesArchiveForm
from django.forms import HiddenInput
from django.utils.text import slugify
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404, redirect
from apps.catalog.forms import CharacterImagesBulkForm, CharacterImagesArchiveForm
from apps.catalog.models import Character, CharacterImage



class HomeTypesView(LoginRequiredMixin, TemplateView):
    '''View для главной страницы с типами произведений.'''
    template_name = "catalog/home_types.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["types"] = Work.TYPE_CHOICES  # <<< ПЕРЕДАЁМ В ШАБЛОН
        return ctx