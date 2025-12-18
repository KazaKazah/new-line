from apps.catalog.views.layout import *


class CharacterCreateView(LoginRequiredMixin, CreateView):
    '''Создание нового персонажа.'''
    model = Character
    form_class = CharacterForm
    template_name = "catalog/form.html"

    # читаем параметры ?work=<slug>&sex=<male|female>
    def _get_work_from_query(self):
        slug = self.request.GET.get("work")
        return get_object_or_404(Work, slug=slug) if slug else None

    def _get_sex_from_query(self):
        sex = self.request.GET.get("sex")
        return sex if sex in dict(Character.SEX_CHOICES) else None

    def get_initial(self):
        initial = super().get_initial()
        w = self._get_work_from_query()
        s = self._get_sex_from_query()
        if w: initial["work"] = w.pk
        if s: initial["sex"] = s
        return initial

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        w = self._get_work_from_query()
        s = self._get_sex_from_query()
        if w:
            form.fields["work"].queryset = Work.objects.filter(pk=w.pk)
            form.fields["work"].widget = HiddenInput()
        if s:
            form.fields["sex"].choices = [(s, dict(Character.SEX_CHOICES)[s])]
            form.fields["sex"].widget = HiddenInput()
        return form

    def _unique_slug(self, base_slug):
        slug = base_slug
        counter = 1
        while Character.objects.filter(slug=slug).exists():
            counter += 1
            slug = f"{base_slug}-{counter}"
        return slug

    def form_valid(self, form):
        w = self._get_work_from_query()
        s = self._get_sex_from_query()
        if w: form.instance.work = w
        if s: form.instance.sex = s

        # Генерация уникального slug
        base_slug = slugify(form.instance.full_name or "")
        if not base_slug:
            base_slug = "character"
        form.instance.slug = self._unique_slug(base_slug)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "characters-by-sex",
            kwargs={"slug": self.object.work.slug, "sex": self.object.sex},
        )
