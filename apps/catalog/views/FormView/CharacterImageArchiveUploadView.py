from apps.catalog.views.layout import *

class CharacterImageArchiveUploadView(LoginRequiredMixin, FormView):
    '''View для загрузки архива с изображениями персонажа.'''
    form_class = CharacterImagesArchiveForm
    template_name = "catalog/character_image_add_archive.html"

    MAX_FILES = 500
    ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

    def dispatch(self, request, *args, **kwargs):
        self.character = get_object_or_404(Character, slug=self.kwargs["slug"])
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self):
        init = super().get_initial()
        init["character"] = self.character.pk
        return init

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["character"] = self.character
        ctx["rar_supported"] = False
        return ctx

    def _is_image_filename(self, name: str) -> bool:
        ext = os.path.splitext(name)[1].lower()
        return ext in self.ALLOWED_EXTS

    def _safe_basename(self, name: str) -> str:
        return PurePosixPath(name).name or "image"

    def _validate_image_bytes(self, data: bytes) -> bytes:
        with Image.open(io.BytesIO(data)) as im:
            im.verify()
        return data

    def form_valid(self, form):
        f = form.files.get("archive")
        caption = form.cleaned_data.get("caption") or ""
        if not f:
            form.add_error("archive", "Загрузите .zip архив.")
            return self.form_invalid(form)

        if not (f.name or "").lower().endswith(".zip"):
            form.add_error("archive", "Поддерживается только .zip.")
            return self.form_invalid(form)

        try:
            with ZipFile(f) as zf:
                names = [n for n in zf.namelist() if not n.endswith("/")]
                names = [n for n in names if self._is_image_filename(n)]
                for i, name in enumerate(names):
                    if i >= self.MAX_FILES:
                        break
                    try:
                        data = zf.read(name)
                        data = self._validate_image_bytes(data)
                        base = self._safe_basename(name)
                        obj = CharacterImage(character=self.character, caption=caption)
                        obj.image.save(base, ContentFile(data), save=True)  # сохраняем файл корректно
                    except (KeyError, UnidentifiedImageError, OSError) as e:
                        # Можно логировать; просто пропускаем плохой файл
                        continue
        except BadZipFile:
            form.add_error("archive", "Файл не является корректным ZIP-архивом.")
            return self.form_invalid(form)

        return redirect("character-gallery", slug=self.character.slug)