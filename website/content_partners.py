# -*- coding: utf-8 -*-
"""Assembler for the "Partners" page (/partners/).

The page gathers ALL partners in one place: the parent company's own partners
(still ``content.PARTNERS`` — home-owned) plus **every subsidiary's partners
read from the CMS database** (``Company.partners_section``). So any partner a
company gains in the admin shows up here automatically. The page's own text and
facts live in the ``PartnersPage`` CMS model.

Logo values are returned as **resolved URLs** (``/static/…`` for the group wall,
``/media/…`` for CMS-managed subsidiary logos); the template renders them
directly with ``{{ logo }}``.
"""
from django.templatetags.static import static as static_url

from . import content
from .models import Company, PartnersPage, _rel, img_url


def partners_page_context():
    page = PartnersPage.load()
    groups = []

    # Holding company (APS) partners — home-owned static logos.
    if content.PARTNERS.get("logos"):
        groups.append({
            "eyebrow": page.t("group_eyebrow"),
            "name": page.t("group_name"),
            "sub": content.PARTNERS.get("subtitle", ""),
            "logos": [static_url(l) for l in content.PARTNERS["logos"]],
        })

    # Each subsidiary's partners (from the CMS database).
    for c in Company.objects.filter(is_published=True):
        sec = _rel(c, "partners_section")
        if sec and sec.logos.exists():
            logos = [img_url(p.image) for p in sec.logos.all()]
            logos = [u for u in logos if u]
            if logos:
                groups.append({
                    "eyebrow": page.t("sub_eyebrow"),
                    "name": c.t("name"),
                    "sub": c.t("sector"),
                    "logos": logos,
                })

    seo = page.seo_context()
    return {
        "page": {"seo": seo, "intro": page.intro_context()},
        "seo": seo,
        "groups": groups,
        "facts": [f.to_context() for f in page.facts.all()],
    }
