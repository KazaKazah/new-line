from django.urls import path
from apps.catalog.views.TemplateView.hometypesview import *
from apps.catalog.views.ListView.GenreWorksView import *
from apps.catalog.views.ListView.WorkListView import *
from apps.catalog.views.ListView.GenreIndexView import *
from apps.catalog.views.ListView.CharacterBySexListView import *
from apps.catalog.views.ListView.CharacterGalleryView import *

from apps.catalog.views.FormView.CharacterImageArchiveUploadView import *
from apps.catalog.views.FormView.CharacterImageBulkCreateView import *

from apps.catalog.views.DetailView.WorkDetailView import *
from apps.catalog.views.DetailView.CharacterDetailView import *

from apps.catalog.views.DeleteView.CharacterImageDeleteView import *

from apps.catalog.views.CreateView.WorkCreateView import *
from apps.catalog.views.CreateView.CharacterCreateView import *
from apps.catalog.views.CreateView.CharacterImageCreateView import *



urlpatterns = [
    path("", HomeTypesView.as_view(), name="home-types"), # главная страница каталога

    path("type/<str:wtype>/", WorkListView.as_view(), name="work-list"), # список произведений по типу
    path("genre/<slug:slug>/", GenreWorksView.as_view(), name="genre-works"),    # список произведений по жанру

    # новая страница "Жанры"
    path("genres/", GenreIndexView.as_view(), name="genre-index"),

    # галерея
    path("character/<slug:slug>/gallery/add/",
         CharacterImageCreateView.as_view(),
         name="character-image-add"),
    path(
        "character/<slug:slug>/gallery/add-multiple/",
        CharacterImageBulkCreateView.as_view(),
        name="character-image-add-multiple",
    ),
    path(
        "character/<slug:slug>/gallery/add-archive/",
        CharacterImageArchiveUploadView.as_view(),
        name="character-image-add-archive",
    ),
    path(
        "character/<slug:slug>/gallery/<int:pk>/delete/",
        CharacterImageDeleteView.as_view(),
        name="character-image-delete",
    ),

    # --- статические пути ВЫШЕ динамических ---
    path("work/add/", WorkCreateView.as_view(), name="work-add"),
    path("character/add/", CharacterCreateView.as_view(), name="character-add"),

    # --- динамические внизу ---
    path("work/<slug:slug>/", WorkDetailView.as_view(), name="work-detail"),
    path("work/<slug:slug>/characters/<str:sex>/",
         CharacterBySexListView.as_view(), name="characters-by-sex"),
    path("character/<slug:slug>/", CharacterDetailView.as_view(), name="character-detail"),
    path("character/<slug:slug>/gallery/",
         CharacterGalleryView.as_view(), name="character-gallery"),
]