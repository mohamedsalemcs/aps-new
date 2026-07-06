# -*- coding: utf-8 -*-
"""Forms for the custom CMS admin (`/manage/`).

Bilingual models expose ``_ar`` / ``_en`` columns; the forms present both so
editors fill Arabic now and English later. Image fields render as file inputs
(upload/replace). Nested content is edited via inline formsets.
"""
from django import forms
from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory

from .models import (
    AboutFact, AboutItem, AboutPage, Company, CompanyFact, ContactChannel,
    ContactOffice, ContactPage, FaqCategory, FaqItem, FaqPage, FaqStat,
    GuidingItem, GuidingSection, HomeContactItem, HomeHeroBadge, HomeHeroSlide,
    HomeIndustry, HomePage, HomePartnerLogo, HomeStat, HomeWhyFeature,
    LifecyclePhase, LifecycleSection, LifecycleStep, PartnerLogo, PartnersFact,
    PartnersPage, PartnersSection, Project, ProjectDetail, ProjectsSection,
    SiteSettings, SystemItem, SystemsSection, SystemTab,
)

_TEXT = forms.TextInput(attrs={"class": "f-in"})
_AREA = forms.Textarea(attrs={"class": "f-in", "rows": 3})

# Friendly destinations for any editable CTA button (value = href). Reuse
# everywhere a button label is editable so editors never type a raw URL.
CTA_CHOICES = [
    ("/#subsidiaries", "قسم الشركات (في الرئيسية)"),
    ("/about/", "صفحة «من نحن»"),
    ("/partners/", "صفحة الشركاء"),
    ("/faq/", "الأسئلة الشائعة"),
    ("/contact/", "تواصل معنا"),
    ("/", "الصفحة الرئيسية"),
]


class _Styled(forms.ModelForm):
    """Apply consistent CSS classes to every widget."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            w = field.widget
            css = w.attrs.get("class", "")
            if isinstance(w, forms.CheckboxInput):
                w.attrs["class"] = (css + " f-check").strip()
            elif isinstance(w, (forms.Select,)):
                w.attrs["class"] = (css + " f-in f-select").strip()
            elif isinstance(w, forms.ClearableFileInput):
                w.attrs["class"] = (css + " f-file").strip()
            else:
                w.attrs["class"] = (css + " f-in").strip()


class GroupForm(_Styled):
    class Meta:
        model = Company._meta.apps.get_model("website", "Group")
        fields = [
            "name_ar", "name_en", "short", "phone", "email", "website",
            "website_url", "location_ar", "location_en", "logo", "logo_footer",
        ]


class ProfileForm(_Styled):
    class Meta:
        model = get_user_model()
        fields = ["first_name", "last_name", "email"]


class SiteSettingsForm(_Styled):
    class Meta:
        model = SiteSettings
        fields = [
            "cta_eyebrow_ar", "cta_eyebrow_en", "cta_title_ar", "cta_title_en",
            "cta_title_hl_ar", "cta_title_hl_en", "cta_subtitle_ar", "cta_subtitle_en",
            "cta_button_ar", "cta_button_en", "cta_offices_label_ar", "cta_offices_label_en",
        ]


# In-page anchor destinations for a company hero button (friendly dropdown).
COMPANY_CTA_CHOICES = [
    ("#systems", "قسم الأنظمة والحلول"),
    ("#projects", "قسم المشاريع"),
    ("#partners", "قسم الشركاء"),
    ("#lifecycle", "قسم دورة الحياة"),
    ("#contact", "قسم التواصل"),
]


class CompanyForm(_Styled):
    class Meta:
        model = Company
        fields = [
            "is_published",
            "name_ar", "name_en", "eyebrow_ar", "eyebrow_en",
            "sector_ar", "sector_en", "logo", "hero_image",
            "hero_cta_ar", "hero_cta_en", "hero_cta_href",
            "about_paragraph_ar", "about_paragraph_en",
            "about_bullets_ar", "about_bullets_en",
            "contact_phone", "contact_email", "contact_website",
            "contact_website_url", "contact_offices_ar", "contact_offices_en",
        ]
        widgets = {
            "about_paragraph_ar": _AREA, "about_paragraph_en": _AREA,
            "about_bullets_ar": _AREA, "about_bullets_en": _AREA,
            "contact_offices_ar": _AREA, "contact_offices_en": _AREA,
            "hero_cta_href": forms.Select(choices=COMPANY_CTA_CHOICES),
            "logo": forms.FileInput(attrs={"accept": "image/*,.svg"}),
            "hero_image": forms.FileInput(attrs={"accept": "image/*,.svg"}),
        }


# --- inline formsets -----------------------------------------------------
def _fs(parent, child, fields, extra=1, **kw):
    return inlineformset_factory(
        parent, child, form=_form_for(child, fields),
        fields=fields, extra=extra, can_delete=True, **kw,
    )


def _form_for(model, fields, widgets=None):
    meta = type("Meta", (), {"model": model, "fields": fields, "widgets": widgets or {}})
    return type(f"{model.__name__}Form", (_Styled,), {"Meta": meta})


def _card_fs(parent, child, fields, widgets=None, **kw):
    """Formset for the card-based editors: no blank extra rows (added via JS),
    hidden ``order`` (implied by card position), and a plain file input."""
    w = {"order": forms.HiddenInput()}
    if "image" in fields:
        w["image"] = forms.FileInput(attrs={"accept": "image/*"})
    w.update(widgets or {})
    return inlineformset_factory(
        parent, child, form=_form_for(child, fields, w),
        fields=fields, extra=kw.pop("extra", 0), can_delete=True, **kw,
    )


FactFormSet = _card_fs(Company, CompanyFact, ["order", "value", "suffix", "label_ar", "label_en"])

SystemsSectionForm = _form_for(SystemsSection, ["mode", "eyebrow_ar", "eyebrow_en", "heading_ar", "heading_en", "subtitle_ar", "subtitle_en"])
_ICON_UP = {"icon_image": forms.FileInput(attrs={"accept": "image/*,.svg"})}
TabFormSet = _card_fs(SystemsSection, SystemTab, ["order", "icon", "icon_image", "title_ar", "title_en"], _ICON_UP)
SystemItemFormSet = _card_fs(SystemsSection, SystemItem, ["order", "tab", "name_ar", "name_en", "image"])

ProjectsSectionForm = _form_for(ProjectsSection, ["detailed", "eyebrow_ar", "eyebrow_en", "heading_ar", "heading_en", "subtitle_ar", "subtitle_en"])
ProjectFormSet = _card_fs(ProjectsSection, Project, ["order", "name_ar", "name_en", "sector_ar", "sector_en", "image"])
ProjectDetailFormSet = _fs(Project, ProjectDetail, ["order", "icon", "label_ar", "label_en", "value_ar", "value_en"])

PartnersSectionForm = _form_for(PartnersSection, ["eyebrow_ar", "eyebrow_en", "heading_ar", "heading_en", "subtitle_ar", "subtitle_en"])
PartnerLogoFormSet = _card_fs(PartnersSection, PartnerLogo, ["order", "name", "image"])

GuidingSectionForm = _form_for(GuidingSection, ["eyebrow_ar", "eyebrow_en", "heading_ar", "heading_en"])
GuidingItemFormSet = _card_fs(GuidingSection, GuidingItem, ["order", "icon", "icon_image", "title_ar", "title_en", "text_ar", "text_en"], _ICON_UP)

LifecycleSectionForm = _form_for(LifecycleSection, ["eyebrow_ar", "eyebrow_en", "heading_ar", "heading_en", "subtitle_ar", "subtitle_en"])
PhaseFormSet = _card_fs(LifecycleSection, LifecyclePhase, ["order", "no", "title_ar", "title_en"])
StepFormSet = _card_fs(LifecyclePhase, LifecycleStep, ["order", "title_ar", "title_en", "text_ar", "text_en"])


# --- About page ----------------------------------------------------------
class AboutPageForm(_Styled):
    class Meta:
        model = AboutPage
        fields = "__all__"


AboutFactFormSet = _card_fs(AboutPage, AboutFact, ["order", "value", "suffix", "label_ar", "label_en"])
AboutItemFormSet = _card_fs(AboutPage, AboutItem, ["order", "icon", "icon_image", "title_ar", "title_en", "text_ar", "text_en"],
                            {"icon_image": forms.FileInput(attrs={"accept": "image/*,.svg"})})

# Per-section forms for the "page as rows" About editor.
AboutIntroForm = _form_for(AboutPage, [
    "intro_eyebrow_ar", "intro_eyebrow_en", "intro_title_ar", "intro_title_en",
    "intro_lead_ar", "intro_lead_en", "intro_bullets_ar", "intro_bullets_en",
    "intro_cta_ar", "intro_cta_en", "intro_cta_href", "intro_image",
    "seo_title_ar", "seo_title_en", "seo_description_ar", "seo_description_en", "seo_image"],
    {"intro_image": forms.FileInput(attrs={"accept": "image/*,.svg"}),
     "intro_cta_href": forms.Select(choices=CTA_CHOICES)})
AboutGuidingHeadForm = _form_for(AboutPage, ["guiding_eyebrow_ar", "guiding_eyebrow_en", "guiding_heading_ar", "guiding_heading_en"])
AboutPrinciplesHeadForm = _form_for(AboutPage, ["principles_eyebrow_ar", "principles_eyebrow_en", "principles_heading_ar", "principles_heading_en", "principles_subtitle_ar", "principles_subtitle_en"])
AboutHseHeadForm = _form_for(AboutPage, ["hse_eyebrow_ar", "hse_eyebrow_en", "hse_heading_ar", "hse_heading_en", "hse_subtitle_ar", "hse_subtitle_en"])


# --- FAQ page ------------------------------------------------------------
class FaqPageForm(_Styled):
    class Meta:
        model = FaqPage
        fields = "__all__"


FaqStatFormSet = _card_fs(FaqPage, FaqStat, ["order", "value", "suffix", "label_ar", "label_en"])
FaqCategoryFormSet = _card_fs(FaqPage, FaqCategory, ["order", "icon", "icon_image", "title_ar", "title_en"], _ICON_UP)
# Nested FAQ editor (each category shown with its own Q&A). extra=1 keeps one
# blank "new category" block ready so a category name + its questions are added
# together in a single save.
FaqCategoryEditFormSet = _card_fs(FaqPage, FaqCategory, ["order", "icon", "icon_image", "title_ar", "title_en"], _ICON_UP, extra=1)
FaqItemFormSet = _card_fs(FaqCategory, FaqItem, ["order", "question_ar", "question_en", "answer_ar", "answer_en"])


# --- Contact page --------------------------------------------------------
class ContactPageForm(_Styled):
    class Meta:
        model = ContactPage
        fields = "__all__"


ContactChannelFormSet = _card_fs(ContactPage, ContactChannel, [
    "order", "icon", "icon_image", "label_ar", "label_en", "value_ar", "value_en",
    "href", "ltr", "note_ar", "note_en"], _ICON_UP)
ContactOfficeFormSet = _card_fs(ContactPage, ContactOffice, [
    "order", "name_ar", "name_en", "tag_ar", "tag_en", "address_ar", "address_en",
    "phone", "email", "map_query", "is_hq"])


# --- Partners page -------------------------------------------------------
class PartnersPageForm(_Styled):
    class Meta:
        model = PartnersPage
        fields = "__all__"


PartnersFactFormSet = _card_fs(PartnersPage, PartnersFact, ["order", "value", "suffix", "label_ar", "label_en"])


# --- Home page (landing) -------------------------------------------------
_IMG_UP = forms.FileInput(attrs={"accept": "image/*,.svg"})

# Per-section header forms (all bind the same HomePage instance, disjoint fields).
HomeHeroForm = _form_for(HomePage, [
    "hero_cta_primary_ar", "hero_cta_primary_en",
    "hero_cta_secondary_ar", "hero_cta_secondary_en"])
HomeAboutForm = _form_for(HomePage, [
    "about_eyebrow_ar", "about_eyebrow_en", "about_heading_ar", "about_heading_en",
    "about_paragraph_ar", "about_paragraph_en", "about_bullets_ar", "about_bullets_en",
    "about_cta_ar", "about_cta_en", "about_cta_href", "about_image", "about_image_secondary",
    "about_badge_num", "about_badge_suffix", "about_badge_text_ar", "about_badge_text_en"],
    {"about_image": _IMG_UP, "about_image_secondary": _IMG_UP,
     "about_cta_href": forms.Select(choices=CTA_CHOICES),
     "about_paragraph_ar": _AREA, "about_paragraph_en": _AREA,
     "about_bullets_ar": _AREA, "about_bullets_en": _AREA})
HomeStatsHeadForm = _form_for(HomePage, [
    "stats_heading_ar", "stats_heading_en", "stats_subtitle_ar", "stats_subtitle_en"],
    {"stats_subtitle_ar": _AREA, "stats_subtitle_en": _AREA})
HomeSubsHeadForm = _form_for(HomePage, [
    "subs_eyebrow_ar", "subs_eyebrow_en", "subs_heading_ar", "subs_heading_en",
    "subs_subtitle_ar", "subs_subtitle_en"],
    {"subs_subtitle_ar": _AREA, "subs_subtitle_en": _AREA})
HomeWhyHeadForm = _form_for(HomePage, [
    "why_eyebrow_ar", "why_eyebrow_en", "why_heading_ar", "why_heading_en",
    "why_subtitle_ar", "why_subtitle_en"],
    {"why_subtitle_ar": _AREA, "why_subtitle_en": _AREA})
HomeIndHeadForm = _form_for(HomePage, [
    "ind_eyebrow_ar", "ind_eyebrow_en", "ind_heading_ar", "ind_heading_en",
    "ind_subtitle_ar", "ind_subtitle_en"],
    {"ind_subtitle_ar": _AREA, "ind_subtitle_en": _AREA})
HomePartnersHeadForm = _form_for(HomePage, [
    "partners_eyebrow_ar", "partners_eyebrow_en", "partners_heading_ar", "partners_heading_en",
    "partners_subtitle_ar", "partners_subtitle_en", "partners_cta_ar", "partners_cta_en",
    "partners_cta_href"],
    {"partners_subtitle_ar": _AREA, "partners_subtitle_en": _AREA,
     "partners_cta_href": forms.Select(choices=CTA_CHOICES)})
HomeContactHeadForm = _form_for(HomePage, [
    "contact_eyebrow_ar", "contact_eyebrow_en", "contact_heading_ar", "contact_heading_en",
    "contact_subtitle_ar", "contact_subtitle_en", "contact_cta_ar", "contact_cta_en",
    "contact_image"],
    {"contact_subtitle_ar": _AREA, "contact_subtitle_en": _AREA, "contact_image": _IMG_UP})
HomeSeoForm = _form_for(HomePage, [
    "seo_title_ar", "seo_title_en", "seo_description_ar", "seo_description_en", "seo_image"])

# Repeatable card formsets.
HomeSlideFormSet = _card_fs(HomePage, HomeHeroSlide, [
    "order", "eyebrow_ar", "eyebrow_en", "title_ar", "title_en",
    "subtitle_ar", "subtitle_en", "layout", "image1", "image2", "image3"],
    {"image1": _IMG_UP, "image2": _IMG_UP, "image3": _IMG_UP})
HomeBadgeFormSet = _card_fs(HomePage, HomeHeroBadge, ["order", "icon", "label_ar", "label_en"])
HomeStatFormSet = _card_fs(HomePage, HomeStat, ["order", "value", "suffix", "label_ar", "label_en"])
HomeWhyFormSet = _card_fs(HomePage, HomeWhyFeature, ["order", "icon", "title_ar", "title_en", "text_ar", "text_en"])
HomeIndustryFormSet = _card_fs(HomePage, HomeIndustry, [
    "order", "icon", "name_ar", "name_en", "image", "tags", "desc_ar", "desc_en"])
HomeLogoFormSet = _card_fs(HomePage, HomePartnerLogo, ["order", "name", "image"])
HomeContactItemFormSet = _card_fs(HomePage, HomeContactItem, [
    "order", "icon", "label_ar", "label_en", "value_ar", "value_en", "href", "ltr"])
