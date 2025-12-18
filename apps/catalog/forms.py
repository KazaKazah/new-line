from django import forms
from django_summernote.widgets import SummernoteWidget  # если уже есть
from .models import Work, Character, CharacterImage, Genre  # + Genre
from django.forms import HiddenInput, ClearableFileInput
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class WorkForm(forms.ModelForm):
    '''Форма для создания и редактирования произведений.'''
    class Meta:
        model = Work
        fields = ["type", "title", "year", "description", "poster", "genres"]
        widgets = {"description": SummernoteWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Сохранить"))


class CharacterForm(forms.ModelForm):
    '''Форма для создания и редактирования персонажей.'''
    class Meta:
        model = Character
        fields = [
            "work", "appearances", "sex", "full_name", "bio", "poster",
            "height_cm", "weight_kg", "age", "race",
            "bust_cm", "hips_cm", "waist_cm",
            "skills", "traits",
        ]
        widgets = {"bio": SummernoteWidget()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Сохранить"))


class CharacterImageForm(forms.ModelForm):
    '''Форма для загрузки изображений персонажей.'''
    class Meta:
        model = CharacterImage
        fields = ["character", "image", "caption"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Загрузить"))


class GenreForm(forms.ModelForm):
    '''Форма для создания и редактирования жанров.'''
    class Meta:
        model = Genre
        fields = ["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Добавить жанр"))


class CharacterImageForm(forms.ModelForm):
    '''Форма для загрузки изображений персонажей.'''
    class Meta:
        model = CharacterImage
        fields = ["character", "image", "caption"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Загрузить"))

    # удобный хелпер, чтобы извне можно было спрятать поле и зафиксировать персонажа
    def bind_character(self, character):
        self.fields["character"].queryset = Character.objects.filter(pk=character.pk)
        self.fields["character"].initial = character.pk
        self.fields["character"].widget = HiddenInput()


class MultipleFileInput(ClearableFileInput):
    allow_multiple_selected = True  # ключевая строка


class CharacterImagesBulkForm(forms.Form):
    '''Форма для массовой загрузки изображений персонажей.'''
    images = forms.FileField(
        label="Файлы изображений",
        widget=MultipleFileInput(attrs={"multiple": True, "accept": "image/*"}),
        required=True,
    )
    caption = forms.CharField(
        label="Подпись (опционально, применится ко всем)",
        max_length=200, required=False
    )
    character = forms.IntegerField(widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Загрузить"))

    def clean(self):
        cleaned = super().clean()
        files = self.files.getlist("images")  # список UploadedFile
        if not files:
            raise forms.ValidationError("Выберите хотя бы одно изображение.")
        for f in files:
            if not getattr(f, "content_type", "").startswith("image/"):
                raise forms.ValidationError("Можно загружать только изображения.")
        cleaned["images_list"] = files  # положим список в cleaned_data
        return cleaned


class CharacterImagesArchiveForm(forms.Form):
    '''Форма для загрузки изображений персонажей из архива.'''
    archive = forms.FileField(
        label="Архив (.zip или .rar)",
        help_text="Рекомендуется .zip",
        widget=forms.ClearableFileInput(attrs={"accept": ".zip,.rar"})
    )
    caption = forms.CharField(
        label="Подпись (опционально, применится ко всем)",
        max_length=200, required=False
    )
    character = forms.IntegerField(widget=HiddenInput())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.add_input(Submit("submit", "Загрузить из архива"))