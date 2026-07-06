"""Sitemaps for the APS Group website.

URLs live under ``i18n_patterns(prefix_default_language=False)``, so ``reverse``
returns the Arabic (root) paths. The framework prepends scheme+host from the
request, so absolute URLs stay correct in every environment. Add an English
sitemap section once the ``/en/`` content is translated (task D).
"""
from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .content_companies import COMPANIES


class StaticViewSitemap(Sitemap):
    """The fixed top-level pages."""
    protocol = "https"
    changefreq = "monthly"

    def items(self):
        return ["website:home", "website:about", "website:partners"]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return 1.0 if item == "website:home" else 0.8


class CompanySitemap(Sitemap):
    """One entry per subsidiary page that actually has content."""
    protocol = "https"
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return list(COMPANIES.keys())

    def location(self, slug):
        return reverse("website:company", args=[slug])


sitemaps = {
    "static": StaticViewSitemap,
    "companies": CompanySitemap,
}
