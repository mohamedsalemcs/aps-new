# -*- coding: utf-8 -*-
"""Browser-language redirect.

Arabic is served at the unprefixed root ("/", the site default) and English at
"/en/". On a visitor's first request (no explicit language choice yet), we look
at the browser's Accept-Language:

* Arabic browser  -> stay on the Arabic root ("/").
* English browser -> redirect to the "/en/" equivalent.
* Any other language (or none) -> default to English ("/en/").

An explicit choice made via the header language switcher sets the
``django_language`` cookie (through Django's ``set_language`` view); once that
cookie exists it takes precedence, so the redirect never fights the user.
"""
from django.http import HttpResponseRedirect
from django.utils.translation.trans_real import parse_accept_lang_header

_SUPPORTED = ("ar", "en")
# "/manage/" is the custom CMS admin: Arabic-only and NOT language-prefixed, so
# it must never be redirected to a non-existent "/en/manage/".
_EXCLUDE_PREFIXES = ("/static/", "/media/", "/admin/", "/i18n/", "/manage/")
_EXCLUDE_EXACT = ("/robots.txt", "/sitemap.xml")


class BrowserLanguageRedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        redirect = self._maybe_redirect(request)
        return redirect if redirect is not None else self.get_response(request)

    def _maybe_redirect(self, request):
        if request.method != "GET":
            return None
        path = request.path_info
        # Already English, or a non-localized utility URL — leave untouched.
        if path == "/en" or path.startswith("/en/"):
            return None
        if path in _EXCLUDE_EXACT or path.startswith(_EXCLUDE_PREFIXES):
            return None

        # Explicit cookie choice wins over browser detection.
        pref = request.COOKIES.get("django_language")
        if pref not in _SUPPORTED:
            pref = self._from_accept_language(request)

        if pref == "ar":
            return None  # Arabic stays on the unprefixed root.

        # English (or any non-Arabic / unknown) -> the /en/ equivalent.
        target = "/en" + path
        query = request.META.get("QUERY_STRING", "")
        if query:
            target = f"{target}?{query}"
        return HttpResponseRedirect(target)

    @staticmethod
    def _from_accept_language(request):
        header = request.META.get("HTTP_ACCEPT_LANGUAGE", "")
        for code, _q in parse_accept_lang_header(header):
            base = code.split("-")[0].lower()
            if base in _SUPPORTED:
                return base
        return "en"  # unknown language -> English default
