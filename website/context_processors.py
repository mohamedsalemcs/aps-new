"""Injects site-wide data (navigation, group info, subsidiaries) into every
template so the shared header and footer render on all pages.

Group identity and the subsidiary list are read from the CMS database
(``Group`` / ``Company``); if the DB hasn't been seeded yet we fall back to the
legacy ``content`` dictionaries so the site never breaks."""
from django.utils.translation import get_language

from . import content
from .models import Company, ContactMessage, Group, SiteSettings


def site_globals(request):
    # Language-aware URL helpers. With i18n_patterns(prefix_default_language=
    # False), Arabic lives at "/" (no prefix) and English at "/en/". Internal
    # links must carry the active language's prefix so navigation keeps the
    # current language instead of falling back to Arabic.
    lang = get_language() or "ar"
    prefix = "" if lang == "ar" else "/" + lang

    # The current path stripped of any language prefix (always starts with "/").
    path = request.path or "/"
    bare = path
    if prefix and path.startswith(prefix):
        bare = path[len(prefix):] or "/"

    group_obj = Group.objects.first()
    group = group_obj.to_context() if group_obj else content.GROUP

    subsidiaries = [c.nav_context() for c in Company.objects.filter(is_published=True)]
    if not subsidiaries:
        subsidiaries = content.SUBSIDIARIES

    # Shared site-wide texts (contact CTA, etc.) — edited once in the CMS.
    site = SiteSettings.load().to_context()

    # Unread inbox badge (only for the staff-facing admin).
    cms_unread = 0
    if path.startswith("/manage/") and getattr(request.user, "is_staff", False):
        cms_unread = ContactMessage.objects.filter(is_read=False).count()

    return {
        "cms_unread": cms_unread,
        "nav": content.NAV,
        "group": group,
        "subsidiaries": subsidiaries,
        "cta": site["cta"],
        "seo_defaults": content.SEO_DEFAULTS,
        # Prefix to prepend to root-relative internal links (e.g. "/en").
        "lang_prefix": prefix,
        # Same page in each language, for the header language switcher.
        "url_ar": bare,
        "url_en": "/en" + bare,
    }
