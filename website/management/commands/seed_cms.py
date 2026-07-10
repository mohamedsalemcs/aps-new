# -*- coding: utf-8 -*-
"""One-off importer: load the legacy Python `content_*` dictionaries into the
CMS database and copy their referenced static images into MEDIA_ROOT.

Run once after migrating:  ``python manage.py seed_cms``

It is **idempotent** — it wipes the Company/Group tables first and rebuilds
them, so it can be re-run safely while iterating. Arabic is activated so the
``gettext_lazy`` strings resolve to their Arabic source; English columns are
left blank (English content isn't authored yet).
"""
import shutil

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import translation

from website import content
from website.content_about import ABOUT_PAGE
from website.content_companies import COMPANIES
from website.content_contact import CONTACT_PAGE
from website.content_faq import FAQ_PAGE
from website.models import (
    AboutFact, AboutItem, AboutPage, Company, CompanyFact, ContactChannel,
    ContactOffice, ContactPage, FaqCategory, FaqItem, FaqPage, FaqStat, Group,
    GuidingItem, GuidingSection, HomeContactItem, HomeHeroBadge, HomeHeroSlide,
    HomeIndustry, HomePage, HomePartnerLogo, HomeStat, HomeWhyFeature,
    LifecyclePhase, LifecycleSection, LifecycleStep, PartnerLogo, PartnersFact,
    PartnersPage, PartnersSection, Project, ProjectDetail, ProjectsSection,
    SiteSettings, SystemItem, SystemsSection, SystemTab,
)

STATIC_DIR = settings.BASE_DIR / "static"


def s(v):
    """Resolve a (possibly lazy) value to a plain string."""
    return "" if v is None else str(v)


class Command(BaseCommand):
    help = "Import legacy content_*.py data into the CMS database."

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.copied = 0
        self.missing = []

    def copy_img(self, rel):
        """Copy static/<rel> -> media/<rel>; return the media-relative name."""
        rel = s(rel)
        if not rel:
            return ""
        src = STATIC_DIR / rel
        if not src.exists():
            self.missing.append(rel)
            return ""
        dst = settings.MEDIA_ROOT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        self.copied += 1
        return rel

    @transaction.atomic
    def handle(self, *args, **options):
        translation.activate("ar")

        # Clean slate (cascades remove all nested section rows).
        Company.objects.all().delete()
        Group.objects.all().delete()
        SiteSettings.objects.all().delete()
        AboutPage.objects.all().delete()
        FaqPage.objects.all().delete()
        ContactPage.objects.all().delete()
        PartnersPage.objects.all().delete()
        HomePage.objects.all().delete()

        SiteSettings.load()  # recreate shared-text defaults
        self._seed_group()
        self._seed_home()
        self._seed_about()
        self._seed_faq()
        self._seed_contact()
        self._seed_partners_page()
        for order, (slug, c) in enumerate(COMPANIES.items()):
            self._seed_company(slug, c, order)

        self.stdout.write(self.style.SUCCESS(
            f"Seeded {Company.objects.count()} companies + group. "
            f"Copied {self.copied} images."
        ))
        if self.missing:
            self.stdout.write(self.style.WARNING(
                f"{len(self.missing)} image(s) not found in static/ (skipped):"
            ))
            for m in self.missing:
                self.stdout.write(f"  - {m}")

    # -- group -------------------------------------------------------------
    def _seed_group(self):
        g = content.GROUP
        Group.objects.create(
            name_ar=s(g["name_ar"]),
            short=s(g["short"]),
            phone=s(g["phone"]),
            email=s(g["email"]),
            website=s(g["website"]),
            website_url=s(g["website_url"]),
            location_ar=s(g["location_ar"]),
            logo=self.copy_img("logos/aps-logo.png"),
            logo_footer=self.copy_img("logos/aps-logo-footer.png"),
        )

    # -- home (landing) ----------------------------------------------------
    def _seed_home(self):
        c = content
        about = c.ABOUT
        seo = c.HOME_SEO
        page = HomePage.objects.create(
            seo_title_ar=s(seo.get("title")), seo_description_ar=s(seo.get("description")),
            seo_image=s(seo.get("image")) or "images/hero/hero-industrial.jpg",
            hero_cta_primary_ar=s(c.HERO_CTA_PRIMARY), hero_cta_secondary_ar=s(c.HERO_CTA_SECONDARY),
            about_eyebrow_ar=s(about.get("eyebrow")), about_heading_ar=s(about.get("heading")),
            about_paragraph_ar=s(about.get("paragraph")),
            about_bullets_ar="\n".join(s(b) for b in about.get("bullets", [])),
            about_cta_ar=s(about.get("cta")), about_cta_href="/about/",
            about_image=self.copy_img(about.get("image")),
            about_image_secondary=self.copy_img(about.get("image_secondary")),
            about_badge_num="25", about_badge_suffix="+",
            about_badge_text_ar="عاماً من الخبرة الصناعية",
            stats_heading_ar=s(c.STATS_HEADING), stats_subtitle_ar=s(c.STATS_SUBTITLE),
            subs_eyebrow_ar="شركات المجموعة", subs_heading_ar=s(c.SUBS_HEADING),
            subs_subtitle_ar=s(c.SUBS_SUBTITLE),
            why_eyebrow_ar="لماذا APS", why_heading_ar=s(c.WHY_HEADING),
            why_subtitle_ar=s(c.WHY_SUBTITLE),
            ind_eyebrow_ar=s(c.INDUSTRIES.get("eyebrow")), ind_heading_ar=s(c.INDUSTRIES.get("heading")),
            ind_subtitle_ar=s(c.INDUSTRIES.get("subtitle")),
            partners_eyebrow_ar=s(c.PARTNERS.get("eyebrow")), partners_heading_ar=s(c.PARTNERS.get("heading")),
            partners_subtitle_ar=s(c.PARTNERS.get("subtitle")), partners_cta_ar=s(c.PARTNERS.get("cta")),
            partners_cta_href="/partners/",
            contact_eyebrow_ar=s(c.CONTACT.get("eyebrow")), contact_heading_ar=s(c.CONTACT.get("heading")),
            contact_subtitle_ar=s(c.CONTACT.get("subtitle")),
            contact_cta_ar="أرسل لنا رسالة", contact_cta_en="Send us a message",
            contact_image=self.copy_img(c.CONTACT.get("image")),
        )
        for i, sl in enumerate(c.HERO_SLIDES):
            imgs = list(sl.get("images", [])) + ["", "", ""]
            HomeHeroSlide.objects.create(
                page=page, order=i, eyebrow_ar=s(sl.get("eyebrow")), title_ar=s(sl.get("title")),
                subtitle_ar=s(sl.get("subtitle")), layout=s(sl.get("layout")) or "single",
                image1=self.copy_img(imgs[0]), image2=self.copy_img(imgs[1]), image3=self.copy_img(imgs[2]),
            )
        for i, b in enumerate(c.HERO_BADGES):
            HomeHeroBadge.objects.create(page=page, order=i, icon=s(b.get("icon")), label_ar=s(b.get("label")))
        for i, st in enumerate(c.STATS):
            HomeStat.objects.create(page=page, order=i, value=s(st.get("value")),
                                    suffix=s(st.get("suffix")), label_ar=s(st.get("label")))
        for i, w in enumerate(c.WHY):
            HomeWhyFeature.objects.create(page=page, order=i, icon=s(w.get("icon")),
                                          title_ar=s(w.get("title")), text_ar=s(w.get("text")))
        for i, it in enumerate(c.INDUSTRIES.get("items", [])):
            HomeIndustry.objects.create(
                page=page, order=i, icon=s(it.get("icon")), name_ar=s(it.get("name")),
                image=self.copy_img(it.get("image")),
                tags="، ".join(s(x) for x in it.get("companies", [])), desc_ar=s(it.get("desc")))
        for i, logo in enumerate(c.PARTNERS.get("logos", [])):
            HomePartnerLogo.objects.create(page=page, order=i, image=self.copy_img(logo))
        for i, it in enumerate(c.CONTACT.get("items", [])):
            HomeContactItem.objects.create(
                page=page, order=i, icon=s(it.get("icon")), label_ar=s(it.get("label")),
                value_ar=s(it.get("value")), href=s(it.get("href")), ltr=bool(it.get("ltr")))

    # -- about -------------------------------------------------------------
    def _seed_about(self):
        a = ABOUT_PAGE
        seo = a.get("seo", {})
        intro = a["intro"]
        g, pr, hse = a["guiding"], a["principles"], a["hse"]
        page = AboutPage.objects.create(
            seo_title_ar=s(seo.get("title")),
            seo_description_ar=s(seo.get("description")),
            seo_image=s(seo.get("image")) or "images/about/hero.jpg",
            intro_eyebrow_ar=s(intro.get("eyebrow")),
            intro_title_ar=s(intro.get("title")),
            intro_lead_ar=s(intro.get("lead")),
            intro_bullets_ar="\n".join(s(b) for b in intro.get("bullets", [])),
            intro_cta_ar=s(intro.get("cta")),
            intro_image=self.copy_img(intro.get("image")),
            guiding_eyebrow_ar=s(g.get("eyebrow")), guiding_heading_ar=s(g.get("heading")),
            principles_eyebrow_ar=s(pr.get("eyebrow")), principles_heading_ar=s(pr.get("heading")),
            principles_subtitle_ar=s(pr.get("subtitle")),
            hse_eyebrow_ar=s(hse.get("eyebrow")), hse_heading_ar=s(hse.get("heading")),
            hse_subtitle_ar=s(hse.get("subtitle")),
        )
        for i, f in enumerate(intro.get("facts", [])):
            AboutFact.objects.create(page=page, order=i, value=s(f.get("value")),
                                     suffix=s(f.get("suffix")), label_ar=s(f.get("label")))
        for group, src in [(AboutItem.GUIDING, g), (AboutItem.PRINCIPLES, pr), (AboutItem.HSE, hse)]:
            for i, it in enumerate(src.get("items", [])):
                AboutItem.objects.create(page=page, group=group, order=i, icon=s(it.get("icon")),
                                         title_ar=s(it.get("title")), text_ar=s(it.get("text")))

    # -- faq ---------------------------------------------------------------
    def _seed_faq(self):
        f = FAQ_PAGE
        seo = f.get("seo", {})
        hero = f["hero"]
        page = FaqPage.objects.create(
            seo_title_ar=s(seo.get("title")), seo_description_ar=s(seo.get("description")),
            hero_eyebrow_ar=s(hero.get("eyebrow")), hero_title_ar=s(hero.get("title")),
            hero_subtitle_ar=s(hero.get("subtitle")),
        )
        for i, st in enumerate(hero.get("stats", [])):
            FaqStat.objects.create(page=page, order=i, value=s(st.get("value")),
                                   suffix=s(st.get("suffix")), label_ar=s(st.get("label")))
        for i, cat in enumerate(f.get("categories", [])):
            c = FaqCategory.objects.create(page=page, order=i, icon=s(cat.get("icon")),
                                           title_ar=s(cat.get("title")))
            for j, qa in enumerate(cat.get("items", [])):
                FaqItem.objects.create(category=c, order=j, question_ar=s(qa.get("q")),
                                       answer_ar=s(qa.get("a")))

    # -- contact -----------------------------------------------------------
    def _seed_contact(self):
        ct = CONTACT_PAGE
        seo = ct.get("seo", {})
        page = ContactPage.objects.create(
            seo_title_ar=s(seo.get("title")), seo_description_ar=s(seo.get("description")),
            eyebrow_ar=s(ct.get("eyebrow")), title_ar=s(ct.get("title")), lead_ar=s(ct.get("lead")),
            subjects_ar="\n".join(s(x) for x in ct.get("subjects", [])),
            offices_heading_ar=s(ct.get("offices_heading")),
            offices_subtitle_ar=s(ct.get("offices_subtitle")),
        )
        for i, ch in enumerate(ct.get("channels", [])):
            ContactChannel.objects.create(
                page=page, order=i, icon=s(ch.get("icon")), label_ar=s(ch.get("label")),
                value_ar=s(ch.get("value")), href=s(ch.get("href")),
                ltr=bool(ch.get("ltr")), note_ar=s(ch.get("note")))
        for i, o in enumerate(ct.get("offices", [])):
            ContactOffice.objects.create(
                page=page, order=i, name_ar=s(o.get("name")), tag_ar=s(o.get("tag")),
                address_ar=s(o.get("address")), phone=s(o.get("phone")), email=s(o.get("email")),
                map_query=s(o.get("map_query")), is_hq=bool(o.get("is_hq")))

    # -- partners page -----------------------------------------------------
    def _seed_partners_page(self):
        page = PartnersPage.objects.create(
            seo_title_ar="شركاؤنا | مجموعة APS — شركاء ومورّدون عالميون",
            seo_description_ar=(
                "شركاء مجموعة APS وشركاتها المتخصصة: نتعاون مع كبرى المصنّعين ومزوّدي "
                "التقنية العالميين عبر قطاعات الأمن والصناعة والمياه والبيئة والتقنيات "
                "المتقدمة في مختلف أنحاء المملكة."
            ),
            seo_image="images/hero/hero-industrial.jpg",
            intro_eyebrow_ar="شركاؤنا",
            intro_title_ar="شبكة شركاء عالمية عبر المجموعة",
            intro_lead_ar=(
                "نجمع في مكانٍ واحد شركاء ومورّدي مجموعة APS وشركاتها المتخصصة — كبرى "
                "العلامات والمصنّعين العالميين الذين نعتمد عليهم لتقديم حلولٍ موثوقة في "
                "الأمن والصناعة والمياه والبيئة والتقنيات المتقدمة."
            ),
        )
        facts = [
            ("200", "+", "شريك ومورّد عالمي"),
            ("5", "", "شركات متخصصة"),
            ("20", "+", "سوق عالمي"),
            ("25", "+", "عاماً من الشراكات"),
        ]
        for i, (value, suffix, label) in enumerate(facts):
            PartnersFact.objects.create(page=page, order=i, value=value, suffix=suffix, label_ar=label)

    # -- company -----------------------------------------------------------
    def _seed_company(self, slug, c, order):
        about = c.get("about", {})
        contact = c.get("contact", {})
        company = Company.objects.create(
            slug=slug,
            order=order,
            name_ar=s(c.get("name")),
            name_en=s(c.get("en")),
            eyebrow_ar=s(c.get("eyebrow")),
            sector_ar=s(c.get("sector")),
            logo=self.copy_img(c.get("logo")),
            hero_image=self.copy_img(c.get("hero_image")),
            hero_cta_ar=s(c.get("hero_cta")),
            hero_cta_href=s(c.get("hero_cta_href")) or "#systems",
            about_paragraph_ar=s(about.get("paragraph")),
            about_bullets_ar="\n".join(s(b) for b in about.get("bullets", [])),
            contact_phone=s(contact.get("phone")),
            contact_email=s(contact.get("email")),
            contact_website=s(contact.get("website")),
            contact_website_url=s(contact.get("website_url")),
            contact_offices_ar="\n".join(s(o) for o in contact.get("offices", [])),
        )

        for i, f in enumerate(c.get("facts", [])):
            CompanyFact.objects.create(
                company=company, order=i,
                value=s(f.get("value")), suffix=s(f.get("suffix")),
                label_ar=s(f.get("label")),
            )

        if "guiding" in c:
            self._seed_guiding(company, c["guiding"])
        if "systems" in c:
            self._seed_systems(company, c["systems"])
        if "projects" in c:
            self._seed_projects(company, c["projects"])
        if "partners" in c:
            self._seed_partners(company, c["partners"])
        if "lifecycle" in c:
            self._seed_lifecycle(company, c["lifecycle"])

    def _seed_guiding(self, company, g):
        sec = GuidingSection.objects.create(
            company=company, eyebrow_ar=s(g.get("eyebrow")), heading_ar=s(g.get("heading")),
        )
        for i, it in enumerate(g.get("items", [])):
            GuidingItem.objects.create(
                section=sec, order=i, icon=s(it.get("icon")),
                title_ar=s(it.get("title")), text_ar=s(it.get("text")),
            )

    def _seed_systems(self, company, sysd):
        mode = SystemsSection.TABS if "tabs" in sysd else SystemsSection.GRID
        sec = SystemsSection.objects.create(
            company=company, mode=mode,
            eyebrow_ar=s(sysd.get("eyebrow")), heading_ar=s(sysd.get("heading")),
            subtitle_ar=s(sysd.get("subtitle")),
        )
        if mode == SystemsSection.TABS:
            for ti, tab in enumerate(sysd.get("tabs", [])):
                t = SystemTab.objects.create(
                    section=sec, order=ti, icon=s(tab.get("icon")), title_ar=s(tab.get("title")),
                )
                for ii, it in enumerate(tab.get("items", [])):
                    SystemItem.objects.create(
                        section=sec, tab=t, order=ii,
                        name_ar=s(it.get("name")), image=self.copy_img(it.get("image")),
                    )
        else:
            for ii, it in enumerate(sysd.get("items", [])):
                SystemItem.objects.create(
                    section=sec, order=ii,
                    name_ar=s(it.get("name")), image=self.copy_img(it.get("image")),
                )

    def _seed_projects(self, company, pd):
        sec = ProjectsSection.objects.create(
            company=company, detailed=bool(pd.get("detailed")),
            eyebrow_ar=s(pd.get("eyebrow")), heading_ar=s(pd.get("heading")),
            subtitle_ar=s(pd.get("subtitle")),
        )
        for i, it in enumerate(pd.get("items", [])):
            proj = Project.objects.create(
                section=sec, order=i,
                name_ar=s(it.get("name")), sector_ar=s(it.get("sector")),
                image=self.copy_img(it.get("image")),
            )
            for di, d in enumerate(it.get("details", [])):
                ProjectDetail.objects.create(
                    project=proj, order=di, icon=s(d.get("icon")),
                    label_ar=s(d.get("label")), value_ar=s(d.get("value")),
                )

    def _seed_partners(self, company, pd):
        sec = PartnersSection.objects.create(
            company=company, eyebrow_ar=s(pd.get("eyebrow")),
            heading_ar=s(pd.get("heading")), subtitle_ar=s(pd.get("subtitle")),
        )
        for i, logo in enumerate(pd.get("logos", [])):
            PartnerLogo.objects.create(section=sec, order=i, image=self.copy_img(logo))

    def _seed_lifecycle(self, company, ld):
        sec = LifecycleSection.objects.create(
            company=company, eyebrow_ar=s(ld.get("eyebrow")),
            heading_ar=s(ld.get("heading")), subtitle_ar=s(ld.get("subtitle")),
        )
        for pi, ph in enumerate(ld.get("phases", [])):
            phase = LifecyclePhase.objects.create(
                section=sec, order=pi, no=s(ph.get("no")), title_ar=s(ph.get("title")),
            )
            for si, st in enumerate(ph.get("steps", [])):
                LifecycleStep.objects.create(
                    phase=phase, order=si,
                    title_ar=s(st.get("title")), text_ar=s(st.get("text")),
                )
