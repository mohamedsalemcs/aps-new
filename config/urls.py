"""URL configuration for the APS Group corporate website.

The default (unprefixed) language is Arabic; English is served under /en/.
"""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from website.sitemaps import sitemaps
from website.views import robots_txt, set_language

# Not language-prefixed: the language switcher, robots.txt and sitemap.xml are
# single canonical URLs. `set_language` is our own view (sets the cookie and
# redirects to `next` verbatim, without re-translating it).
urlpatterns = [
    path('i18n/setlang/', set_language, name='set_language'),
    path('robots.txt', robots_txt, name='robots'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    # Custom CMS admin (Arabic, not language-prefixed).
    path('manage/', include('website.cms_urls')),
]

# Language-prefixed routes. prefix_default_language=False keeps Arabic at the
# site root ("/") and serves English at "/en/".
urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('', include('website.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.BASE_DIR / 'static')
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
