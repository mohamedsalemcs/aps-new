# -*- coding: utf-8 -*-
"""CMS models for the APS Group website.

Phase 1 covers the **Group identity** and the **subsidiary companies** (with
their nested systems / projects / partners / guiding / lifecycle sections).

Design notes
------------
* **Bilingual** — every editorial string has ``_ar`` and ``_en`` columns. The
  ``pick()`` helper returns the field for the active language and falls back to
  Arabic when the English value is empty (English content isn't authored yet).
* **Images** are ``ImageField`` uploads served from ``MEDIA_ROOT``. Editors
  upload/replace them from the custom admin.
* Each model exposes ``to_context()`` (or is assembled by ``Company.to_context``)
  producing **exactly** the dict shape the existing templates already consume,
  so the front-end templates barely change.
"""
from django.db import models
from django.utils.translation import get_language
from django.utils.translation import gettext_lazy as _


# --- helpers -------------------------------------------------------------
def pick(ar, en):
    """Return the value for the active language, falling back to Arabic."""
    if (get_language() or "ar").startswith("en"):
        return en or ar
    return ar or en


def lines(text):
    """Split a newline-separated textarea into a clean list of items."""
    return [ln.strip() for ln in (text or "").splitlines() if ln.strip()]


def img_url(field):
    """Media URL for an ImageField, or '' when empty."""
    return field.url if field and getattr(field, "name", "") else ""


def latest_update(base_dt, *querysets):
    """Most-recent ``updated_at`` across a base timestamp and related querysets.

    Lets a page/company report when *any* of its content (own row or children)
    was last edited, so the dashboard's "last updated" reflects section edits too.
    """
    dts = [base_dt]
    for qs in querysets:
        dts.append(qs.aggregate(_m=models.Max("updated_at"))["_m"])
    dts = [d for d in dts if d]
    return max(dts) if dts else None


class Bilingual(models.Model):
    """Mixin: ``t('title')`` -> localized value of ``title_ar`` / ``title_en``.

    Also stamps ``updated_at`` on every save (auto_now) so the CMS dashboard can
    show when each page/section was last edited. Nullable: existing rows created
    before this field was added read NULL until their next save.
    """

    updated_at = models.DateTimeField(_("آخر تحديث"), auto_now=True, null=True, editable=False)

    class Meta:
        abstract = True

    def t(self, base):
        return pick(getattr(self, base + "_ar", ""), getattr(self, base + "_en", ""))


# --- Group identity (singleton) -----------------------------------------
class Group(Bilingual):
    """The parent holding company (APS). One row; drives header/footer/CTA."""

    name_ar = models.CharField(_("اسم المجموعة (عربي)"), max_length=200)
    name_en = models.CharField(_("اسم المجموعة (إنجليزي)"), max_length=200, blank=True)
    short = models.CharField(_("الاختصار"), max_length=20, default="APS")
    phone = models.CharField(_("الهاتف"), max_length=40)
    email = models.EmailField(_("البريد الإلكتروني"))
    website = models.CharField(_("الموقع (نص)"), max_length=120, blank=True)
    website_url = models.URLField(_("رابط الموقع"), blank=True)
    location_ar = models.CharField(_("الموقع الجغرافي (عربي)"), max_length=200, blank=True)
    location_en = models.CharField(_("الموقع الجغرافي (إنجليزي)"), max_length=200, blank=True)
    logo = models.ImageField(_("الشعار (الهيدر)"), upload_to="group/", blank=True)
    logo_footer = models.ImageField(_("الشعار (الفوتر - أبيض)"), upload_to="group/", blank=True)

    class Meta:
        verbose_name = _("هوية المجموعة")
        verbose_name_plural = _("هوية المجموعة")

    def __str__(self):
        return self.short or self.name_ar

    def to_context(self):
        return {
            "name_ar": self.name_ar,
            "name": self.t("name"),
            "short": self.short,
            "phone": self.phone,
            "email": self.email,
            "website": self.website,
            "website_url": self.website_url,
            "location_ar": self.t("location"),
            "logo": img_url(self.logo),
            "logo_footer": img_url(self.logo_footer),
        }


# --- Site-wide settings (singleton) -------------------------------------
class SiteSettings(Bilingual):
    """Shared texts that appear identically across pages (edited once).

    Currently the site-wide "Contact CTA" band shown at the bottom of the
    company/about pages. More shared strings can be added here later.
    """

    cta_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, default="ابقَ على تواصل")
    cta_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    cta_title_ar = models.CharField(_("العنوان (عربي)"), max_length=200, default="تواصل مع فريقنا للاستفسارات")
    cta_title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    cta_title_hl_ar = models.CharField(_("الكلمة المميّزة (عربي)"), max_length=80, default="والدعم")
    cta_title_hl_en = models.CharField(_("الكلمة المميّزة (إنجليزي)"), max_length=80, blank=True)
    cta_subtitle_ar = models.TextField(_("الوصف (عربي)"), default="يستجيب فريقنا بسرعة بحلولٍ احترافية مصمّمة خصيصاً لتلبية احتياجاتك الكهروميكانيكية والصناعية.")
    cta_subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)
    cta_button_ar = models.CharField(_("نص الزر (عربي)"), max_length=80, default="تواصل معنا")
    cta_button_en = models.CharField(_("نص الزر (إنجليزي)"), max_length=80, blank=True)
    cta_offices_label_ar = models.CharField(_("كلمة \"مكاتبنا\" (عربي)"), max_length=40, default="مكاتبنا:")
    cta_offices_label_en = models.CharField(_("كلمة \"مكاتبنا\" (إنجليزي)"), max_length=40, blank=True)

    class Meta:
        verbose_name = _("إعدادات الموقع")
        verbose_name_plural = _("إعدادات الموقع")

    def __str__(self):
        return "إعدادات الموقع"

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj

    def to_context(self):
        return {
            "cta": {
                "eyebrow": self.t("cta_eyebrow"),
                "title": self.t("cta_title"),
                "title_hl": self.t("cta_title_hl"),
                "subtitle": self.t("cta_subtitle"),
                "button": self.t("cta_button"),
                "offices_label": self.t("cta_offices_label"),
            },
        }


# --- Company (subsidiary) ------------------------------------------------
class Company(Bilingual):
    slug = models.SlugField(_("المُعرّف (slug)"), unique=True)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    is_published = models.BooleanField(_("منشورة"), default=True)

    name_ar = models.CharField(_("الاسم (عربي)"), max_length=200)
    name_en = models.CharField(_("الاسم (إنجليزي)"), max_length=200, blank=True)
    eyebrow_ar = models.CharField(_("العنوان الفرعي (عربي)"), max_length=120, blank=True)
    eyebrow_en = models.CharField(_("العنوان الفرعي (إنجليزي)"), max_length=120, blank=True)
    sector_ar = models.CharField(_("القطاع (عربي)"), max_length=160, blank=True)
    sector_en = models.CharField(_("القطاع (إنجليزي)"), max_length=160, blank=True)

    logo = models.ImageField(_("شعار الشركة"), upload_to="companies/logos/", blank=True)
    hero_image = models.ImageField(_("صورة الواجهة"), upload_to="companies/hero/", blank=True)
    hero_cta_ar = models.CharField(_("زر الواجهة (عربي)"), max_length=80, blank=True)
    hero_cta_en = models.CharField(_("زر الواجهة (إنجليزي)"), max_length=80, blank=True)
    hero_cta_href = models.CharField(_("رابط زر الواجهة"), max_length=80, default="#systems")

    about_paragraph_ar = models.TextField(_("نبذة (عربي)"), blank=True)
    about_paragraph_en = models.TextField(_("نبذة (إنجليزي)"), blank=True)
    about_bullets_ar = models.TextField(_("نقاط النبذة (عربي، سطر لكل نقطة)"), blank=True)
    about_bullets_en = models.TextField(_("نقاط النبذة (إنجليزي، سطر لكل نقطة)"), blank=True)

    contact_phone = models.CharField(_("هاتف التواصل"), max_length=40, blank=True)
    contact_email = models.EmailField(_("بريد التواصل"), blank=True)
    contact_website = models.CharField(_("الموقع (نص)"), max_length=120, blank=True)
    contact_website_url = models.URLField(_("رابط الموقع"), blank=True)
    contact_offices_ar = models.TextField(_("المكاتب (عربي، سطر لكل مكتب)"), blank=True)
    contact_offices_en = models.TextField(_("المكاتب (إنجليزي، سطر لكل مكتب)"), blank=True)

    class Meta:
        verbose_name = _("شركة")
        verbose_name_plural = _("الشركات")
        ordering = ["order", "id"]

    def __str__(self):
        return self.name_ar

    @property
    def last_updated(self):
        return latest_update(
            self.updated_at,
            self.facts.all(),
            SystemItem.objects.filter(section__company=self),
            Project.objects.filter(section__company=self),
            GuidingItem.objects.filter(section__company=self),
            LifecyclePhase.objects.filter(section__company=self),
        )

    # -- context assembly --------------------------------------------------
    def _breadcrumb(self):
        return [
            {"label": _("الرئيسية"), "href": "/"},
            {"label": _("شركات المجموعة"), "href": "/#subsidiaries"},
            {"label": self.t("name")},
        ]

    def to_context(self):
        data = {
            "slug": self.slug,
            "name": self.t("name"),
            "en": self.name_en,
            "eyebrow": self.t("eyebrow"),
            "sector": self.t("sector"),
            "logo": img_url(self.logo),
            "hero_image": img_url(self.hero_image),
            "hero_cta": self.t("hero_cta"),
            "hero_cta_href": self.hero_cta_href,
            "breadcrumb": self._breadcrumb(),
            "about": {
                "paragraph": self.t("about_paragraph"),
                "bullets": lines(pick(self.about_bullets_ar, self.about_bullets_en)),
            },
            "facts": [f.to_context() for f in self.facts.all()],
            "contact": {
                "phone": self.contact_phone,
                "email": self.contact_email,
                "website": self.contact_website,
                "website_url": self.contact_website_url,
                "offices": lines(pick(self.contact_offices_ar, self.contact_offices_en)),
            },
        }

        # Optional sections — included only when they actually have content, so
        # an auto-created but empty section never renders an empty band.
        guiding = _rel(self, "guiding_section")
        if guiding and guiding.items.exists():
            data["guiding"] = guiding.to_context()
        systems = _rel(self, "systems_section")
        if systems and (systems.tabs.exists() or systems.items.exists()):
            data["systems"] = systems.to_context()
        projects = _rel(self, "projects_section")
        if projects and projects.items.exists():
            data["projects"] = projects.to_context()
        partners = _rel(self, "partners_section")
        if partners and partners.logos.exists():
            data["partners"] = partners.to_context()
        lifecycle = _rel(self, "lifecycle_section")
        if lifecycle and lifecycle.phases.exists():
            data["lifecycle"] = lifecycle.to_context()
        return data

    def nav_context(self):
        """Lightweight shape for the header dropdown / footer list."""
        return {
            "slug": self.slug,
            "name": self.t("name"),
            "en": self.name_en,
            "sector": self.t("sector"),
        }


def _rel(obj, name):
    """Return a reverse OneToOne related object or None if it doesn't exist."""
    try:
        return getattr(obj, name)
    except models.ObjectDoesNotExist:
        return None


class CompanyFact(Bilingual):
    company = models.ForeignKey(Company, related_name="facts", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    value = models.CharField(_("القيمة"), max_length=20)
    suffix = models.CharField(_("اللاحقة"), max_length=10, blank=True)
    label_ar = models.CharField(_("الوصف (عربي)"), max_length=120)
    label_en = models.CharField(_("الوصف (إنجليزي)"), max_length=120, blank=True)

    class Meta:
        verbose_name = _("رقم/حقيقة")
        verbose_name_plural = _("الأرقام والحقائق")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value}{self.suffix}"

    def to_context(self):
        return {"value": self.value, "suffix": self.suffix, "label": self.t("label")}


# --- Systems / solutions section ----------------------------------------
class SystemsSection(Bilingual):
    TABS = "tabs"
    GRID = "grid"
    MODE_CHOICES = [(TABS, _("تبويبات")), (GRID, _("شبكة"))]

    company = models.OneToOneField(Company, related_name="systems_section", on_delete=models.CASCADE)
    mode = models.CharField(_("العرض"), max_length=8, choices=MODE_CHOICES, default=GRID)
    eyebrow_ar = models.CharField(_("العنوان الفرعي (عربي)"), max_length=120, blank=True)
    eyebrow_en = models.CharField(_("العنوان الفرعي (إنجليزي)"), max_length=120, blank=True)
    heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("قسم الأنظمة والحلول")
        verbose_name_plural = _("أقسام الأنظمة والحلول")

    def __str__(self):
        return f"{self.company.name_ar} — {self.t('heading')}"

    def to_context(self):
        ctx = {
            "eyebrow": self.t("eyebrow"),
            "heading": self.t("heading"),
            "subtitle": self.t("subtitle"),
        }
        if self.mode == self.TABS:
            ctx["tabs"] = [tab.to_context() for tab in self.tabs.all()]
        else:
            ctx["items"] = [it.to_context() for it in self.items.filter(tab__isnull=True)]
        return ctx


class SystemTab(Bilingual):
    section = models.ForeignKey(SystemsSection, related_name="tabs", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    icon = models.CharField(_("اسم أيقونة جاهزة"), max_length=40, blank=True)
    icon_image = models.ImageField(_("أيقونة مرفوعة (PNG/SVG)"), upload_to="companies/systems/icons/", blank=True)
    title_ar = models.CharField(_("العنوان (عربي)"), max_length=160)
    title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=160, blank=True)

    class Meta:
        verbose_name = _("تبويب أنظمة")
        verbose_name_plural = _("تبويبات الأنظمة")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_ar

    def to_context(self):
        return {
            "icon": self.icon,
            "icon_image": img_url(self.icon_image),
            "title": self.t("title"),
            "items": [it.to_context() for it in self.items.all()],
        }


class SystemItem(Bilingual):
    section = models.ForeignKey(SystemsSection, related_name="items", on_delete=models.CASCADE)
    tab = models.ForeignKey(SystemTab, related_name="items", on_delete=models.CASCADE, null=True, blank=True)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    name_ar = models.CharField(_("الاسم (عربي)"), max_length=200)
    name_en = models.CharField(_("الاسم (إنجليزي)"), max_length=200, blank=True)
    image = models.ImageField(_("الصورة"), upload_to="companies/systems/", blank=True)

    class Meta:
        verbose_name = _("عنصر نظام")
        verbose_name_plural = _("عناصر الأنظمة")
        ordering = ["order", "id"]

    def __str__(self):
        return self.name_ar

    def to_context(self):
        return {"name": self.t("name"), "image": img_url(self.image)}


# --- Projects section ----------------------------------------------------
class ProjectsSection(Bilingual):
    company = models.OneToOneField(Company, related_name="projects_section", on_delete=models.CASCADE)
    detailed = models.BooleanField(_("بطاقات تفصيلية"), default=False)
    eyebrow_ar = models.CharField(_("العنوان الفرعي (عربي)"), max_length=120, blank=True)
    eyebrow_en = models.CharField(_("العنوان الفرعي (إنجليزي)"), max_length=120, blank=True)
    heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("قسم المشاريع")
        verbose_name_plural = _("أقسام المشاريع")

    def __str__(self):
        return f"{self.company.name_ar} — {self.t('heading')}"

    def to_context(self):
        return {
            "eyebrow": self.t("eyebrow"),
            "heading": self.t("heading"),
            "subtitle": self.t("subtitle"),
            "detailed": self.detailed,
            "items": [p.to_context() for p in self.items.all()],
        }


class Project(Bilingual):
    section = models.ForeignKey(ProjectsSection, related_name="items", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    name_ar = models.CharField(_("الاسم (عربي)"), max_length=200)
    name_en = models.CharField(_("الاسم (إنجليزي)"), max_length=200, blank=True)
    sector_ar = models.CharField(_("القطاع/الجهة (عربي)"), max_length=160, blank=True)
    sector_en = models.CharField(_("القطاع/الجهة (إنجليزي)"), max_length=160, blank=True)
    image = models.ImageField(_("الصورة"), upload_to="companies/projects/", blank=True)

    class Meta:
        verbose_name = _("مشروع")
        verbose_name_plural = _("المشاريع")
        ordering = ["order", "id"]

    def __str__(self):
        return self.name_ar

    def to_context(self):
        ctx = {
            "name": self.t("name"),
            "sector": self.t("sector"),
            "image": img_url(self.image),
        }
        details = [d.to_context() for d in self.details.all()]
        if details:
            ctx["details"] = details
        return ctx


class ProjectDetail(Bilingual):
    project = models.ForeignKey(Project, related_name="details", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    icon = models.CharField(_("الأيقونة"), max_length=40, blank=True)
    label_ar = models.CharField(_("التسمية (عربي)"), max_length=120)
    label_en = models.CharField(_("التسمية (إنجليزي)"), max_length=120, blank=True)
    value_ar = models.CharField(_("القيمة (عربي)"), max_length=160)
    value_en = models.CharField(_("القيمة (إنجليزي)"), max_length=160, blank=True)

    class Meta:
        verbose_name = _("تفصيل مشروع")
        verbose_name_plural = _("تفاصيل المشاريع")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.label_ar}: {self.value_ar}"

    def to_context(self):
        return {"icon": self.icon, "label": self.t("label"), "value": self.t("value")}


# --- Partners section ----------------------------------------------------
class PartnersSection(Bilingual):
    company = models.OneToOneField(Company, related_name="partners_section", on_delete=models.CASCADE)
    eyebrow_ar = models.CharField(_("العنوان الفرعي (عربي)"), max_length=120, blank=True)
    eyebrow_en = models.CharField(_("العنوان الفرعي (إنجليزي)"), max_length=120, blank=True)
    heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("قسم الشركاء")
        verbose_name_plural = _("أقسام الشركاء")

    def __str__(self):
        return f"{self.company.name_ar} — {self.t('heading')}"

    def to_context(self):
        return {
            "eyebrow": self.t("eyebrow"),
            "heading": self.t("heading"),
            "subtitle": self.t("subtitle"),
            "logos": [img_url(p.image) for p in self.logos.all() if img_url(p.image)],
        }


class PartnerLogo(models.Model):
    section = models.ForeignKey(PartnersSection, related_name="logos", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    name = models.CharField(_("اسم الشريك"), max_length=120, blank=True)
    image = models.ImageField(_("الشعار"), upload_to="companies/partners/", blank=True)

    class Meta:
        verbose_name = _("شعار شريك")
        verbose_name_plural = _("شعارات الشركاء")
        ordering = ["order", "id"]

    def __str__(self):
        return self.name or f"logo #{self.pk}"


# --- Guiding (Vision / Mission) section ----------------------------------
class GuidingSection(Bilingual):
    company = models.OneToOneField(Company, related_name="guiding_section", on_delete=models.CASCADE)
    eyebrow_ar = models.CharField(_("العنوان الفرعي (عربي)"), max_length=120, blank=True)
    eyebrow_en = models.CharField(_("العنوان الفرعي (إنجليزي)"), max_length=120, blank=True)
    heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)

    class Meta:
        verbose_name = _("قسم المبادئ التوجيهية")
        verbose_name_plural = _("أقسام المبادئ التوجيهية")

    def __str__(self):
        return f"{self.company.name_ar} — {self.t('heading')}"

    def to_context(self):
        return {
            "eyebrow": self.t("eyebrow"),
            "heading": self.t("heading"),
            "items": [it.to_context() for it in self.items.all()],
        }


class GuidingItem(Bilingual):
    section = models.ForeignKey(GuidingSection, related_name="items", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    icon = models.CharField(_("اسم أيقونة جاهزة"), max_length=40, blank=True)
    icon_image = models.ImageField(_("أيقونة مرفوعة (PNG/SVG)"), upload_to="companies/guiding/icons/", blank=True)
    title_ar = models.CharField(_("العنوان (عربي)"), max_length=160)
    title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=160, blank=True)
    text_ar = models.TextField(_("النص (عربي)"))
    text_en = models.TextField(_("النص (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("عنصر مبدأ توجيهي")
        verbose_name_plural = _("عناصر المبادئ التوجيهية")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_ar

    def to_context(self):
        return {"icon": self.icon, "icon_image": img_url(self.icon_image),
                "title": self.t("title"), "text": self.t("text")}


# --- Lifecycle (phased timeline) section ---------------------------------
class LifecycleSection(Bilingual):
    company = models.OneToOneField(Company, related_name="lifecycle_section", on_delete=models.CASCADE)
    eyebrow_ar = models.CharField(_("العنوان الفرعي (عربي)"), max_length=120, blank=True)
    eyebrow_en = models.CharField(_("العنوان الفرعي (إنجليزي)"), max_length=120, blank=True)
    heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("قسم دورة الحياة")
        verbose_name_plural = _("أقسام دورة الحياة")

    def __str__(self):
        return f"{self.company.name_ar} — {self.t('heading')}"

    def to_context(self):
        return {
            "eyebrow": self.t("eyebrow"),
            "heading": self.t("heading"),
            "subtitle": self.t("subtitle"),
            "phases": [ph.to_context() for ph in self.phases.all()],
        }


class LifecyclePhase(Bilingual):
    section = models.ForeignKey(LifecycleSection, related_name="phases", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    no = models.CharField(_("الرقم"), max_length=8, blank=True)
    title_ar = models.CharField(_("العنوان (عربي)"), max_length=160)
    title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=160, blank=True)

    class Meta:
        verbose_name = _("مرحلة")
        verbose_name_plural = _("مراحل دورة الحياة")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_ar

    def to_context(self):
        return {
            "no": self.no,
            "title": self.t("title"),
            "steps": [s.to_context() for s in self.steps.all()],
        }


class LifecycleStep(Bilingual):
    phase = models.ForeignKey(LifecyclePhase, related_name="steps", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    title_ar = models.CharField(_("العنوان (عربي)"), max_length=160)
    title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=160, blank=True)
    text_ar = models.TextField(_("النص (عربي)"))
    text_en = models.TextField(_("النص (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("خطوة")
        verbose_name_plural = _("خطوات المراحل")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_ar

    def to_context(self):
        return {"title": self.t("title"), "text": self.t("text")}


# --- About page (singleton) ---------------------------------------------
class AboutPage(Bilingual):
    """The "من نحن / About" page: intro + facts + guiding + principles + HSE."""

    seo_title_ar = models.CharField(_("عنوان SEO (عربي)"), max_length=200, blank=True)
    seo_title_en = models.CharField(_("عنوان SEO (إنجليزي)"), max_length=200, blank=True)
    seo_description_ar = models.TextField(_("وصف SEO (عربي)"), blank=True)
    seo_description_en = models.TextField(_("وصف SEO (إنجليزي)"), blank=True)
    seo_image = models.CharField(_("صورة SEO (مسار)"), max_length=200, default="images/about/hero.jpg")

    intro_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    intro_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    intro_title_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    intro_title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    intro_lead_ar = models.TextField(_("المقدمة (عربي)"), blank=True)
    intro_lead_en = models.TextField(_("المقدمة (إنجليزي)"), blank=True)
    intro_bullets_ar = models.TextField(_("نقاط (عربي، سطر لكل نقطة)"), blank=True)
    intro_bullets_en = models.TextField(_("نقاط (إنجليزي، سطر لكل نقطة)"), blank=True)
    intro_cta_ar = models.CharField(_("نص الزر (عربي)"), max_length=80, blank=True)
    intro_cta_en = models.CharField(_("نص الزر (إنجليزي)"), max_length=80, blank=True)
    intro_cta_href = models.CharField(_("رابط الزر"), max_length=200, default="/#subsidiaries", blank=True)
    intro_image = models.ImageField(_("صورة المقدمة"), upload_to="about/", blank=True)

    guiding_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    guiding_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    guiding_heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    guiding_heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)

    principles_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    principles_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    principles_heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    principles_heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    principles_subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    principles_subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    hse_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    hse_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    hse_heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    hse_heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    hse_subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    hse_subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("صفحة من نحن")
        verbose_name_plural = _("صفحة من نحن")

    def __str__(self):
        return "صفحة من نحن"

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj

    def _items(self, group):
        return [it.to_context() for it in self.items.filter(group=group)]

    @property
    def last_updated(self):
        return latest_update(self.updated_at, self.facts.all(), self.items.all())

    def to_context(self):
        return {
            "seo": {
                "title": self.t("seo_title"),
                "description": self.t("seo_description"),
                "image": self.seo_image,
                "type": "website",
            },
            "intro": {
                "breadcrumb": [{"label": _("الرئيسية"), "href": "/"}, {"label": _("من نحن")}],
                "eyebrow": self.t("intro_eyebrow"),
                "title": self.t("intro_title"),
                "lead": self.t("intro_lead"),
                "bullets": lines(pick(self.intro_bullets_ar, self.intro_bullets_en)),
                "cta": self.t("intro_cta"),
                "cta_href": self.intro_cta_href or "/#subsidiaries",
                "image": img_url(self.intro_image),
                "facts": [f.to_context() for f in self.facts.all()],
            },
            "guiding": {
                "eyebrow": self.t("guiding_eyebrow"),
                "heading": self.t("guiding_heading"),
                "items": self._items(AboutItem.GUIDING),
            },
            "principles": {
                "eyebrow": self.t("principles_eyebrow"),
                "heading": self.t("principles_heading"),
                "subtitle": self.t("principles_subtitle"),
                "items": self._items(AboutItem.PRINCIPLES),
            },
            "hse": {
                "eyebrow": self.t("hse_eyebrow"),
                "heading": self.t("hse_heading"),
                "subtitle": self.t("hse_subtitle"),
                "items": self._items(AboutItem.HSE),
            },
        }


class AboutFact(Bilingual):
    page = models.ForeignKey(AboutPage, related_name="facts", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    value = models.CharField(_("القيمة"), max_length=20)
    suffix = models.CharField(_("اللاحقة"), max_length=10, blank=True)
    label_ar = models.CharField(_("الوصف (عربي)"), max_length=120)
    label_en = models.CharField(_("الوصف (إنجليزي)"), max_length=120, blank=True)

    class Meta:
        verbose_name = _("رقم (من نحن)")
        verbose_name_plural = _("أرقام من نحن")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value}{self.suffix}"

    def to_context(self):
        return {"value": self.value, "suffix": self.suffix, "label": self.t("label")}


class AboutItem(Bilingual):
    GUIDING, PRINCIPLES, HSE = "guiding", "principles", "hse"
    GROUP_CHOICES = [(GUIDING, _("الرؤية والرسالة")), (PRINCIPLES, _("مبادئ العمل")), (HSE, _("الصحة والسلامة"))]

    page = models.ForeignKey(AboutPage, related_name="items", on_delete=models.CASCADE)
    group = models.CharField(_("القسم"), max_length=12, choices=GROUP_CHOICES)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    icon = models.CharField(_("اسم أيقونة جاهزة"), max_length=40, blank=True)
    icon_image = models.ImageField(_("أيقونة مرفوعة (PNG/SVG)"), upload_to="about/icons/", blank=True)
    title_ar = models.CharField(_("العنوان (عربي)"), max_length=160)
    title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=160, blank=True)
    text_ar = models.TextField(_("النص (عربي)"))
    text_en = models.TextField(_("النص (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("عنصر (من نحن)")
        verbose_name_plural = _("عناصر من نحن")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_ar

    def to_context(self):
        return {"icon": self.icon, "icon_image": img_url(self.icon_image),
                "title": self.t("title"), "text": self.t("text")}


# --- FAQ page (singleton) ------------------------------------------------
class FaqPage(Bilingual):
    seo_title_ar = models.CharField(_("عنوان SEO (عربي)"), max_length=200, blank=True)
    seo_title_en = models.CharField(_("عنوان SEO (إنجليزي)"), max_length=200, blank=True)
    seo_description_ar = models.TextField(_("وصف SEO (عربي)"), blank=True)
    seo_description_en = models.TextField(_("وصف SEO (إنجليزي)"), blank=True)
    hero_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    hero_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    hero_title_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    hero_title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    hero_subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    hero_subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("صفحة الأسئلة الشائعة")
        verbose_name_plural = _("صفحة الأسئلة الشائعة")

    def __str__(self):
        return "صفحة الأسئلة الشائعة"

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj

    @property
    def last_updated(self):
        return latest_update(
            self.updated_at, self.stats.all(), self.categories.all(),
            FaqItem.objects.filter(category__page=self),
        )

    def to_context(self):
        return {
            "seo": {"title": self.t("seo_title"), "description": self.t("seo_description"), "type": "website"},
            "hero": {
                "eyebrow": self.t("hero_eyebrow"),
                "title": self.t("hero_title"),
                "subtitle": self.t("hero_subtitle"),
                "breadcrumb": [{"label": _("الرئيسية"), "href": "/"}, {"label": _("الأسئلة الشائعة")}],
                "stats": [st.to_context() for st in self.stats.all()],
            },
            "categories": [c.to_context() for c in self.categories.all()],
        }


class FaqStat(Bilingual):
    page = models.ForeignKey(FaqPage, related_name="stats", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    value = models.CharField(_("القيمة"), max_length=20)
    suffix = models.CharField(_("اللاحقة"), max_length=10, blank=True)
    label_ar = models.CharField(_("الوصف (عربي)"), max_length=120)
    label_en = models.CharField(_("الوصف (إنجليزي)"), max_length=120, blank=True)

    class Meta:
        verbose_name = _("رقم (FAQ)")
        verbose_name_plural = _("أرقام FAQ")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value}{self.suffix}"

    def to_context(self):
        return {"value": self.value, "suffix": self.suffix, "label": self.t("label")}


class FaqCategory(Bilingual):
    page = models.ForeignKey(FaqPage, related_name="categories", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    icon = models.CharField(_("اسم أيقونة جاهزة"), max_length=40, blank=True)
    icon_image = models.ImageField(_("أيقونة مرفوعة (PNG/SVG)"), upload_to="faq/icons/", blank=True)
    title_ar = models.CharField(_("العنوان (عربي)"), max_length=160)
    title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=160, blank=True)

    class Meta:
        verbose_name = _("فئة FAQ")
        verbose_name_plural = _("فئات FAQ")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_ar

    def to_context(self):
        return {
            "icon": self.icon,
            "icon_image": img_url(self.icon_image),
            "title": self.t("title"),
            "items": [it.to_context() for it in self.items.all()],
        }


class FaqItem(Bilingual):
    category = models.ForeignKey(FaqCategory, related_name="items", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    question_ar = models.CharField(_("السؤال (عربي)"), max_length=300)
    question_en = models.CharField(_("السؤال (إنجليزي)"), max_length=300, blank=True)
    answer_ar = models.TextField(_("الجواب (عربي)"))
    answer_en = models.TextField(_("الجواب (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("سؤال FAQ")
        verbose_name_plural = _("أسئلة FAQ")
        ordering = ["order", "id"]

    def __str__(self):
        return self.question_ar

    def to_context(self):
        return {"q": self.t("question"), "a": self.t("answer")}


# --- Contact page (singleton) -------------------------------------------
class ContactPage(Bilingual):
    seo_title_ar = models.CharField(_("عنوان SEO (عربي)"), max_length=200, blank=True)
    seo_title_en = models.CharField(_("عنوان SEO (إنجليزي)"), max_length=200, blank=True)
    seo_description_ar = models.TextField(_("وصف SEO (عربي)"), blank=True)
    seo_description_en = models.TextField(_("وصف SEO (إنجليزي)"), blank=True)
    eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    title_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    lead_ar = models.TextField(_("المقدمة (عربي)"), blank=True)
    lead_en = models.TextField(_("المقدمة (إنجليزي)"), blank=True)
    subjects_ar = models.TextField(_("مواضيع الرسالة (عربي، سطر لكل موضوع)"), blank=True)
    subjects_en = models.TextField(_("مواضيع الرسالة (إنجليزي، سطر لكل موضوع)"), blank=True)
    offices_heading_ar = models.CharField(_("عنوان المكاتب (عربي)"), max_length=200, blank=True)
    offices_heading_en = models.CharField(_("عنوان المكاتب (إنجليزي)"), max_length=200, blank=True)
    offices_subtitle_ar = models.TextField(_("وصف المكاتب (عربي)"), blank=True)
    offices_subtitle_en = models.TextField(_("وصف المكاتب (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("صفحة تواصل معنا")
        verbose_name_plural = _("صفحة تواصل معنا")

    def __str__(self):
        return "صفحة تواصل معنا"

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj

    @property
    def last_updated(self):
        return latest_update(self.updated_at, self.channels.all(), self.offices.all())

    def to_context(self):
        return {
            "seo": {"title": self.t("seo_title"), "description": self.t("seo_description"), "type": "website"},
            "breadcrumb": [{"label": _("الرئيسية"), "href": "/"}, {"label": _("تواصل معنا")}],
            "eyebrow": self.t("eyebrow"),
            "title": self.t("title"),
            "lead": self.t("lead"),
            "channels": [ch.to_context() for ch in self.channels.all()],
            "subjects": lines(pick(self.subjects_ar, self.subjects_en)),
            "offices_heading": self.t("offices_heading"),
            "offices_subtitle": self.t("offices_subtitle"),
            "offices": [o.to_context() for o in self.offices.all()],
        }


class ContactChannel(Bilingual):
    page = models.ForeignKey(ContactPage, related_name="channels", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    icon = models.CharField(_("اسم أيقونة جاهزة"), max_length=40, blank=True)
    icon_image = models.ImageField(_("أيقونة مرفوعة (PNG/SVG)"), upload_to="contact/icons/", blank=True)
    label_ar = models.CharField(_("التسمية (عربي)"), max_length=120)
    label_en = models.CharField(_("التسمية (إنجليزي)"), max_length=120, blank=True)
    value_ar = models.CharField(_("القيمة (عربي)"), max_length=200)
    value_en = models.CharField(_("القيمة (إنجليزي)"), max_length=200, blank=True)
    href = models.CharField(_("الرابط (tel:/mailto:)"), max_length=200, blank=True)
    ltr = models.BooleanField(_("اتجاه LTR (أرقام/لاتيني)"), default=False)
    note_ar = models.CharField(_("ملاحظة (عربي)"), max_length=200, blank=True)
    note_en = models.CharField(_("ملاحظة (إنجليزي)"), max_length=200, blank=True)

    class Meta:
        verbose_name = _("قناة تواصل")
        verbose_name_plural = _("قنوات التواصل")
        ordering = ["order", "id"]

    def __str__(self):
        return self.label_ar

    def to_context(self):
        return {
            "icon": self.icon, "icon_image": img_url(self.icon_image),
            "label": self.t("label"), "value": self.t("value"),
            "href": self.href, "ltr": self.ltr, "note": self.t("note"),
        }


class ContactOffice(Bilingual):
    page = models.ForeignKey(ContactPage, related_name="offices", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    name_ar = models.CharField(_("الاسم (عربي)"), max_length=120)
    name_en = models.CharField(_("الاسم (إنجليزي)"), max_length=120, blank=True)
    tag_ar = models.CharField(_("الوسم (عربي)"), max_length=80, blank=True)
    tag_en = models.CharField(_("الوسم (إنجليزي)"), max_length=80, blank=True)
    address_ar = models.TextField(_("العنوان (عربي)"), blank=True)
    address_en = models.TextField(_("العنوان (إنجليزي)"), blank=True)
    phone = models.CharField(_("الهاتف"), max_length=40, blank=True)
    email = models.EmailField(_("البريد"), blank=True)
    map_query = models.CharField(_("استعلام الخريطة"), max_length=200, blank=True)
    is_hq = models.BooleanField(_("المقر الرئيسي"), default=False)

    class Meta:
        verbose_name = _("مكتب")
        verbose_name_plural = _("المكاتب")
        ordering = ["order", "id"]

    def __str__(self):
        return self.name_ar

    def to_context(self):
        return {
            "name": self.t("name"), "tag": self.t("tag"), "address": self.t("address"),
            "phone": self.phone, "email": self.email, "map_query": self.map_query, "is_hq": self.is_hq,
        }


# --- Partners page (singleton) ------------------------------------------
class PartnersPage(Bilingual):
    """The /partners/ page's own text + facts. The partner logo walls are
    assembled dynamically (holding company + each subsidiary's partners)."""

    seo_title_ar = models.CharField(_("عنوان SEO (عربي)"), max_length=200, blank=True)
    seo_title_en = models.CharField(_("عنوان SEO (إنجليزي)"), max_length=200, blank=True)
    seo_description_ar = models.TextField(_("وصف SEO (عربي)"), blank=True)
    seo_description_en = models.TextField(_("وصف SEO (إنجليزي)"), blank=True)
    seo_image = models.CharField(_("صورة SEO (مسار)"), max_length=200, default="images/hero/hero-industrial.jpg")

    intro_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    intro_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    intro_title_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    intro_title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    intro_lead_ar = models.TextField(_("المقدمة (عربي)"), blank=True)
    intro_lead_en = models.TextField(_("المقدمة (إنجليزي)"), blank=True)

    group_eyebrow_ar = models.CharField(_("وسم المجموعة القابضة (عربي)"), max_length=120, default="الشركة القابضة")
    group_eyebrow_en = models.CharField(_("وسم المجموعة القابضة (إنجليزي)"), max_length=120, blank=True)
    group_name_ar = models.CharField(_("اسم المجموعة (عربي)"), max_length=160, default="مجموعة APS")
    group_name_en = models.CharField(_("اسم المجموعة (إنجليزي)"), max_length=160, blank=True)
    sub_eyebrow_ar = models.CharField(_("وسم الشركات التابعة (عربي)"), max_length=120, default="شركة تابعة")
    sub_eyebrow_en = models.CharField(_("وسم الشركات التابعة (إنجليزي)"), max_length=120, blank=True)

    class Meta:
        verbose_name = _("صفحة الشركاء")
        verbose_name_plural = _("صفحة الشركاء")

    def __str__(self):
        return "صفحة الشركاء"

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj

    @property
    def last_updated(self):
        return latest_update(self.updated_at, self.facts.all())

    def intro_context(self):
        return {
            "breadcrumb": [{"label": _("الرئيسية"), "href": "/"}, {"label": _("الشركاء")}],
            "eyebrow": self.t("intro_eyebrow"),
            "title": self.t("intro_title"),
            "lead": self.t("intro_lead"),
        }

    def seo_context(self):
        return {
            "title": self.t("seo_title"),
            "description": self.t("seo_description"),
            "image": self.seo_image,
            "type": "website",
        }


class PartnersFact(Bilingual):
    page = models.ForeignKey(PartnersPage, related_name="facts", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    value = models.CharField(_("القيمة"), max_length=20)
    suffix = models.CharField(_("اللاحقة"), max_length=10, blank=True)
    label_ar = models.CharField(_("الوصف (عربي)"), max_length=120)
    label_en = models.CharField(_("الوصف (إنجليزي)"), max_length=120, blank=True)

    class Meta:
        verbose_name = _("رقم (الشركاء)")
        verbose_name_plural = _("أرقام الشركاء")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value}{self.suffix}"

    def to_context(self):
        return {"value": self.value, "suffix": self.suffix, "label": self.t("label")}


# --- Home page (singleton) ----------------------------------------------
class HomePage(Bilingual):
    """The public landing page (``/``): hero slider, about lookback, stats,
    subsidiaries header, "why APS", industries marquee, partners, contact.

    Repeatable content (slides, badges, stats, features, industries, logos,
    contact items) lives in child models. Subsidiary *cards* are NOT stored
    here — they read from :class:`Company`; only this section's heading/subtitle
    are editable. ``to_context`` returns exactly the dict shape ``home.html``
    already consumes."""

    # SEO
    seo_title_ar = models.CharField(_("عنوان SEO (عربي)"), max_length=200, blank=True)
    seo_title_en = models.CharField(_("عنوان SEO (إنجليزي)"), max_length=200, blank=True)
    seo_description_ar = models.TextField(_("وصف SEO (عربي)"), blank=True)
    seo_description_en = models.TextField(_("وصف SEO (إنجليزي)"), blank=True)
    seo_image = models.CharField(_("صورة SEO (مسار)"), max_length=200, default="images/hero/hero-industrial.jpg")

    # Hero
    hero_cta_primary_ar = models.CharField(_("الزر الرئيسي (عربي)"), max_length=80, blank=True)
    hero_cta_primary_en = models.CharField(_("الزر الرئيسي (إنجليزي)"), max_length=80, blank=True)
    hero_cta_secondary_ar = models.CharField(_("الزر الثانوي (عربي)"), max_length=80, blank=True)
    hero_cta_secondary_en = models.CharField(_("الزر الثانوي (إنجليزي)"), max_length=80, blank=True)

    # About (home lookback band)
    about_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    about_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    about_heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    about_heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    about_paragraph_ar = models.TextField(_("الفقرة (عربي)"), blank=True)
    about_paragraph_en = models.TextField(_("الفقرة (إنجليزي)"), blank=True)
    about_bullets_ar = models.TextField(_("نقاط (عربي، سطر لكل نقطة)"), blank=True)
    about_bullets_en = models.TextField(_("نقاط (إنجليزي، سطر لكل نقطة)"), blank=True)
    about_cta_ar = models.CharField(_("نص الزر (عربي)"), max_length=80, blank=True)
    about_cta_en = models.CharField(_("نص الزر (إنجليزي)"), max_length=80, blank=True)
    about_cta_href = models.CharField(_("رابط الزر"), max_length=200, default="/about/", blank=True)
    about_image = models.ImageField(_("الصورة الرئيسية"), upload_to="home/", blank=True)
    about_image_secondary = models.ImageField(_("الصورة الثانوية"), upload_to="home/", blank=True)
    about_badge_num = models.CharField(_("رقم الشارة"), max_length=10, default="25", blank=True)
    about_badge_suffix = models.CharField(_("لاحقة الشارة"), max_length=10, default="+", blank=True)
    about_badge_text_ar = models.CharField(_("نص الشارة (عربي)"), max_length=120, blank=True)
    about_badge_text_en = models.CharField(_("نص الشارة (إنجليزي)"), max_length=120, blank=True)

    # Stats
    stats_heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    stats_heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    stats_subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    stats_subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    # Subsidiaries (cards come from Company; only the header is editable here)
    subs_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    subs_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    subs_heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    subs_heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    subs_subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    subs_subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    # Why APS
    why_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    why_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    why_heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    why_heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    why_subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    why_subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    # Industries
    ind_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    ind_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    ind_heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    ind_heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    ind_subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    ind_subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    # Partners
    partners_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    partners_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    partners_heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    partners_heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    partners_subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    partners_subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)
    partners_cta_ar = models.CharField(_("نص الزر (عربي)"), max_length=80, blank=True)
    partners_cta_en = models.CharField(_("نص الزر (إنجليزي)"), max_length=80, blank=True)
    partners_cta_href = models.CharField(_("رابط الزر"), max_length=200, default="/partners/", blank=True)

    # Contact band
    contact_eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=120, blank=True)
    contact_eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=120, blank=True)
    contact_heading_ar = models.CharField(_("العنوان (عربي)"), max_length=200, blank=True)
    contact_heading_en = models.CharField(_("العنوان (إنجليزي)"), max_length=200, blank=True)
    contact_subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    contact_subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)
    contact_cta_ar = models.CharField(_("نص الزر (عربي)"), max_length=80, blank=True)
    contact_cta_en = models.CharField(_("نص الزر (إنجليزي)"), max_length=80, blank=True)
    contact_image = models.ImageField(_("صورة القسم"), upload_to="home/", blank=True)

    class Meta:
        verbose_name = _("الصفحة الرئيسية")
        verbose_name_plural = _("الصفحة الرئيسية")

    def __str__(self):
        return "الصفحة الرئيسية"

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create()
        return obj

    @property
    def last_updated(self):
        return latest_update(
            self.updated_at, self.hero_slides.all(), self.hero_badges.all(),
            self.stats.all(), self.why_features.all(), self.industries.all(),
            self.partner_logos.all(), self.contact_items.all(),
        )

    def to_context(self):
        return {
            "seo": {
                "title": self.t("seo_title"),
                "description": self.t("seo_description"),
                "image": self.seo_image,
                "type": "website",
            },
            "hero_slides": [s.to_context() for s in self.hero_slides.all()],
            "hero_badges": [b.to_context() for b in self.hero_badges.all()],
            "hero_cta_primary": self.t("hero_cta_primary"),
            "hero_cta_secondary": self.t("hero_cta_secondary"),
            "about": {
                "eyebrow": self.t("about_eyebrow"),
                "heading": self.t("about_heading"),
                "paragraph": self.t("about_paragraph"),
                "bullets": lines(pick(self.about_bullets_ar, self.about_bullets_en)),
                "cta": self.t("about_cta"),
                "cta_href": self.about_cta_href or "/about/",
                "image": img_url(self.about_image),
                "image_secondary": img_url(self.about_image_secondary),
                "badge_num": self.about_badge_num,
                "badge_suffix": self.about_badge_suffix,
                "badge_text": self.t("about_badge_text"),
            },
            "stats_heading": self.t("stats_heading"),
            "stats_subtitle": self.t("stats_subtitle"),
            "stats": [st.to_context() for st in self.stats.all()],
            "subs_eyebrow": self.t("subs_eyebrow"),
            "subs_heading": self.t("subs_heading"),
            "subs_subtitle": self.t("subs_subtitle"),
            "why_eyebrow": self.t("why_eyebrow"),
            "why_heading": self.t("why_heading"),
            "why_subtitle": self.t("why_subtitle"),
            "why": [f.to_context() for f in self.why_features.all()],
            "industries": {
                "eyebrow": self.t("ind_eyebrow"),
                "heading": self.t("ind_heading"),
                "subtitle": self.t("ind_subtitle"),
                "items": [it.to_context() for it in self.industries.all()],
            },
            "partners": {
                "eyebrow": self.t("partners_eyebrow"),
                "heading": self.t("partners_heading"),
                "subtitle": self.t("partners_subtitle"),
                "cta": self.t("partners_cta"),
                "cta_href": self.partners_cta_href or "/partners/",
                "logos": [img_url(l.image) for l in self.partner_logos.all() if l.image],
            },
            "contact": {
                "eyebrow": self.t("contact_eyebrow"),
                "heading": self.t("contact_heading"),
                "subtitle": self.t("contact_subtitle"),
                "cta": self.t("contact_cta"),
                "image": img_url(self.contact_image),
                "items": [c.to_context() for c in self.contact_items.all()],
            },
        }


class HomeHeroSlide(Bilingual):
    CLUSTER, SINGLE, DUO = "cluster", "single", "duo"
    LAYOUT_CHOICES = [(CLUSTER, _("ثلاث صور (عنقود)")), (SINGLE, _("صورة واحدة")), (DUO, _("صورتان"))]

    page = models.ForeignKey(HomePage, related_name="hero_slides", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    eyebrow_ar = models.CharField(_("سطر علوي (عربي)"), max_length=160, blank=True)
    eyebrow_en = models.CharField(_("سطر علوي (إنجليزي)"), max_length=160, blank=True)
    title_ar = models.CharField(_("العنوان (عربي)"), max_length=240)
    title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=240, blank=True)
    subtitle_ar = models.TextField(_("الوصف (عربي)"), blank=True)
    subtitle_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)
    layout = models.CharField(_("نمط الصور"), max_length=10, choices=LAYOUT_CHOICES, default=SINGLE)
    image1 = models.ImageField(_("الصورة 1"), upload_to="home/hero/", blank=True)
    image2 = models.ImageField(_("الصورة 2"), upload_to="home/hero/", blank=True)
    image3 = models.ImageField(_("الصورة 3"), upload_to="home/hero/", blank=True)

    class Meta:
        verbose_name = _("شريحة (الهيرو)")
        verbose_name_plural = _("شرائح الهيرو")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_ar

    def to_context(self):
        imgs = [img_url(i) for i in (self.image1, self.image2, self.image3) if i]
        return {
            "eyebrow": self.t("eyebrow"), "title": self.t("title"),
            "subtitle": self.t("subtitle"), "layout": self.layout, "images": imgs,
        }


class HomeHeroBadge(Bilingual):
    page = models.ForeignKey(HomePage, related_name="hero_badges", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    icon = models.CharField(_("اسم أيقونة"), max_length=40, blank=True)
    label_ar = models.CharField(_("النص (عربي)"), max_length=120)
    label_en = models.CharField(_("النص (إنجليزي)"), max_length=120, blank=True)

    class Meta:
        verbose_name = _("شارة (الهيرو)")
        verbose_name_plural = _("شارات الهيرو")
        ordering = ["order", "id"]

    def __str__(self):
        return self.label_ar

    def to_context(self):
        return {"icon": self.icon, "label": self.t("label")}


class HomeStat(Bilingual):
    page = models.ForeignKey(HomePage, related_name="stats", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    value = models.CharField(_("القيمة"), max_length=20)
    suffix = models.CharField(_("اللاحقة"), max_length=10, blank=True)
    label_ar = models.CharField(_("الوصف (عربي)"), max_length=120)
    label_en = models.CharField(_("الوصف (إنجليزي)"), max_length=120, blank=True)

    class Meta:
        verbose_name = _("رقم (الرئيسية)")
        verbose_name_plural = _("أرقام الرئيسية")
        ordering = ["order", "id"]

    def __str__(self):
        return f"{self.value}{self.suffix}"

    def to_context(self):
        return {"value": self.value, "suffix": self.suffix, "label": self.t("label")}


class HomeWhyFeature(Bilingual):
    page = models.ForeignKey(HomePage, related_name="why_features", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    icon = models.CharField(_("اسم أيقونة"), max_length=40, blank=True)
    title_ar = models.CharField(_("العنوان (عربي)"), max_length=160)
    title_en = models.CharField(_("العنوان (إنجليزي)"), max_length=160, blank=True)
    text_ar = models.TextField(_("النص (عربي)"))
    text_en = models.TextField(_("النص (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("ميزة (لماذا APS)")
        verbose_name_plural = _("مزايا لماذا APS")
        ordering = ["order", "id"]

    def __str__(self):
        return self.title_ar

    def to_context(self):
        return {"icon": self.icon, "title": self.t("title"), "text": self.t("text")}


class HomeIndustry(Bilingual):
    page = models.ForeignKey(HomePage, related_name="industries", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    icon = models.CharField(_("اسم أيقونة"), max_length=40, blank=True)
    name_ar = models.CharField(_("الاسم (عربي)"), max_length=160)
    name_en = models.CharField(_("الاسم (إنجليزي)"), max_length=160, blank=True)
    image = models.ImageField(_("الصورة"), upload_to="home/industries/", blank=True)
    tags = models.CharField(_("شركات المجموعة (وسوم، افصل بفاصلة)"), max_length=200, blank=True)
    desc_ar = models.TextField(_("الوصف (عربي)"))
    desc_en = models.TextField(_("الوصف (إنجليزي)"), blank=True)

    class Meta:
        verbose_name = _("قطاع (الرئيسية)")
        verbose_name_plural = _("قطاعات الرئيسية")
        ordering = ["order", "id"]

    def __str__(self):
        return self.name_ar

    def to_context(self):
        tags = [t.strip() for t in (self.tags or "").replace("،", ",").split(",") if t.strip()]
        return {"icon": self.icon, "name": self.t("name"), "image": img_url(self.image),
                "companies": tags, "desc": self.t("desc")}


class HomePartnerLogo(models.Model):
    page = models.ForeignKey(HomePage, related_name="partner_logos", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    name = models.CharField(_("اسم الشريك"), max_length=120, blank=True)
    image = models.ImageField(_("الشعار"), upload_to="home/partners/", blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, editable=False)

    class Meta:
        verbose_name = _("شعار شريك (الرئيسية)")
        verbose_name_plural = _("شعارات الشركاء (الرئيسية)")
        ordering = ["order", "id"]

    def __str__(self):
        return self.name or f"logo-{self.pk}"


class HomeContactItem(Bilingual):
    page = models.ForeignKey(HomePage, related_name="contact_items", on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("الترتيب"), default=0)
    icon = models.CharField(_("اسم أيقونة"), max_length=40, blank=True)
    label_ar = models.CharField(_("العنوان (عربي)"), max_length=120)
    label_en = models.CharField(_("العنوان (إنجليزي)"), max_length=120, blank=True)
    value_ar = models.CharField(_("القيمة (عربي)"), max_length=200)
    value_en = models.CharField(_("القيمة (إنجليزي)"), max_length=200, blank=True)
    href = models.CharField(_("الرابط (tel:/mailto: أو عنوان)"), max_length=200, blank=True)
    ltr = models.BooleanField(_("عرض بالإنجليزية (LTR)"), default=False)

    class Meta:
        verbose_name = _("بطاقة تواصل (الرئيسية)")
        verbose_name_plural = _("بطاقات التواصل (الرئيسية)")
        ordering = ["order", "id"]

    def __str__(self):
        return self.label_ar

    def to_context(self):
        return {"icon": self.icon, "label": self.t("label"), "value": self.t("value"),
                "href": self.href, "ltr": self.ltr}


# --- Contact form submissions (inbox) -----------------------------------
class ContactMessage(models.Model):
    name = models.CharField(_("الاسم"), max_length=160)
    email = models.EmailField(_("البريد الإلكتروني"))
    phone = models.CharField(_("الهاتف"), max_length=60, blank=True)
    company = models.CharField(_("الشركة"), max_length=160, blank=True)
    subjects = models.CharField(_("المواضيع"), max_length=300, blank=True)
    message = models.TextField(_("الرسالة"))
    is_read = models.BooleanField(_("مقروءة"), default=False)
    created_at = models.DateTimeField(_("التاريخ"), auto_now_add=True)

    class Meta:
        verbose_name = _("رسالة تواصل")
        verbose_name_plural = _("صندوق الوارد")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.created_at:%Y-%m-%d}"
