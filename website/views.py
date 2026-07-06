from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.templatetags.static import static
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from . import content


@require_POST
def set_language(request):
    """Persist the chosen language in a cookie and redirect to ``next`` exactly.

    Unlike Django's built-in ``set_language`` we do NOT re-translate ``next``:
    the header switcher already provides the precise target URL (``url_ar`` /
    ``url_en``), so translating it would send an Arabic switch to the English
    URL. The cookie makes the choice stick against the browser-language
    auto-redirect middleware.
    """
    lang = request.POST.get("language", "")
    next_url = request.POST.get("next") or "/"
    if not url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        next_url = "/"
    response = HttpResponseRedirect(next_url)
    if lang in dict(settings.LANGUAGES):
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME, lang,
            max_age=60 * 60 * 24 * 365,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
    return response
from .content_about import ABOUT_PAGE
from .content_companies import COMPANIES
from .content_contact import CONTACT_PAGE
from .content_faq import FAQ_PAGE
from .content_partners import partners_page_context
from .models import AboutPage, Company, ContactMessage, ContactPage, FaqPage, Group, HomePage, img_url


def home(request):
    """Home with the new single full-bleed hero (default)."""
    return render(request, 'home.html', _home_ctx(request, 'solo'))


def home_slider(request):
    """Alternate home with the classic multi-slide hero — lets the client
    compare the two hero versions live, side by side."""
    return render(request, 'home.html', _home_ctx(request, 'slider'))


def _home_ctx(request, hero_variant):
    ctx = content.home_context()
    ctx['hero_variant'] = hero_variant
    # The home page is CMS-managed: overlay the DB content (hero, about, stats,
    # subsidiaries header, why, industries, partners, contact, SEO) over the
    # legacy defaults. Falls back to the legacy dict if the page isn't seeded.
    hp = HomePage.objects.first()
    if hp is not None:
        ctx.update(hp.to_context())
    # The home context still carries the legacy GROUP dict; prefer the CMS-edited
    # Group so identity edits (phone/email/logo) show on the home page too.
    group = Group.objects.first()
    if group is not None:
        ctx['group'] = group.to_context()
    # Company name / English name / sector are edited in the CMS — make the home
    # "subsidiaries" section read them from the DB so the name is a single source
    # of truth: the header dropdown, this home section, and the company detail
    # page all show the same name, and a CMS rename propagates to all three.
    # The home card's landscape image and short description have no CMS field, so
    # they stay from the legacy content keyed by slug (falling back to the
    # company's own hero image / about paragraph for any company added later).
    companies = list(Company.objects.filter(is_published=True))
    if companies:
        legacy = {s['slug']: s for s in content.SUBSIDIARIES}
        subs = []
        for c in companies:
            extra = legacy.get(c.slug, {})
            subs.append({
                **c.nav_context(),  # slug, name, en, sector — from the CMS
                'image': static(extra['image']) if extra.get('image') else img_url(c.hero_image),
                'desc': extra.get('desc') or c.t('about_paragraph'),
            })
        ctx['subsidiaries'] = subs
    return ctx


def about(request):
    page = AboutPage.load().to_context()
    return render(request, 'about.html', {'page': page, 'seo': page.get('seo')})


def _deliver_contact_message(form):
    """Best-effort email of a contact submission. Never raises: if no mail
    backend is configured (dev), the submission is still accepted by the view."""
    subjects = "، ".join(form["subjects"]) or "استفسار عام"
    body = (
        f"الاسم: {form['name']}\n"
        f"البريد الإلكتروني: {form['email']}\n"
        f"الهاتف: {form['phone'] or '—'}\n"
        f"الشركة: {form['company'] or '—'}\n"
        f"الموضوع: {subjects}\n\n"
        f"الرسالة:\n{form['message']}\n"
    )
    try:
        send_mail(
            subject=f"[نموذج تواصل] {subjects} — {form['name']}",
            message=body,
            from_email=None,  # DEFAULT_FROM_EMAIL
            recipient_list=[content.GROUP["email"]],
            fail_silently=True,
        )
    except Exception:
        pass


def contact(request):
    page = ContactPage.load().to_context()
    ctx = {"page": page, "seo": page.get("seo")}
    if request.method == "POST":
        form = {
            "name": request.POST.get("name", "").strip(),
            "email": request.POST.get("email", "").strip(),
            "phone": request.POST.get("phone", "").strip(),
            "company": request.POST.get("company", "").strip(),
            "subjects": request.POST.getlist("subjects"),
            "message": request.POST.get("message", "").strip(),
        }
        errors = {}
        if not form["name"]:
            errors["name"] = "يُرجى إدخال الاسم."
        if not form["email"]:
            errors["email"] = "يُرجى إدخال البريد الإلكتروني."
        else:
            try:
                validate_email(form["email"])
            except ValidationError:
                errors["email"] = "يُرجى إدخال بريد إلكتروني صحيح."
        if not form["message"]:
            errors["message"] = "يُرجى كتابة محتوى رسالتك."
        if errors:
            ctx["errors"] = errors
            ctx["form"] = form
        else:
            ContactMessage.objects.create(
                name=form["name"], email=form["email"], phone=form["phone"],
                company=form["company"], subjects="، ".join(form["subjects"]),
                message=form["message"],
            )
            _deliver_contact_message(form)
            ctx["sent"] = True
            ctx["sent_name"] = form["name"]
    return render(request, "contact.html", ctx)


def partners(request):
    return render(request, 'partners.html', partners_page_context())


def faq(request):
    page = FaqPage.load().to_context()
    return render(request, 'faq.html', {'page': page, 'seo': page.get('seo')})


def company(request, slug):
    obj = Company.objects.filter(slug=slug, is_published=True).first()
    if obj is None:
        raise Http404("Company not found")
    return render(request, 'company.html', {'company': obj.to_context()})


def robots_txt(request):
    """Plain-text robots.txt with an absolute sitemap URL for the host."""
    sitemap_url = request.build_absolute_uri('/sitemap.xml')
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "",
        f"Sitemap: {sitemap_url}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain; charset=utf-8")
