# -*- coding: utf-8 -*-
"""Custom CMS admin views (`/manage/`).

A lightweight, Arabic, RTL editing surface for non-technical staff. Auth uses
Django's session auth; every editing view requires a logged-in staff user.
"""
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.core.paginator import Paginator
from django.db.models import Max
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import slugify

from . import cms_forms as F
from .models import (
    AboutItem, AboutPage, Company, ContactMessage, ContactPage, FaqCategory,
    FaqPage, GuidingSection, Group, HomePage, LifecyclePhase, LifecycleSection,
    PartnersPage, PartnersSection, Project, ProjectsSection, SiteSettings,
    SystemsSection, _rel,
)


def staff_required(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        u = request.user
        if not (u.is_authenticated and u.is_staff):
            return redirect(f"/manage/login/?next={request.path}")
        return view(request, *args, **kwargs)
    return wrapper


# --- auth ---------------------------------------------------------------
def login_view(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect("cms:dashboard")
    error = None
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_staff:
                login(request, user)
                nxt = request.GET.get("next") or "/manage/"
                return redirect(nxt)
            error = "هذا الحساب لا يملك صلاحية الدخول إلى لوحة التحكم."
        else:
            error = "اسم المستخدم أو كلمة المرور غير صحيحة."
    return render(request, "manage/login.html", {"error": error})


def logout_view(request):
    logout(request)
    return redirect("cms:login")


@staff_required
def profile(request):
    user = request.user
    pform = F.ProfileForm(instance=user)
    pwform = PasswordChangeForm(user)
    if request.method == "POST":
        if "save_profile" in request.POST:
            pform = F.ProfileForm(request.POST, instance=user)
            if pform.is_valid():
                pform.save()
                messages.success(request, "تم حفظ بيانات الملف الشخصي.")
                return redirect("cms:profile")
        elif "change_password" in request.POST:
            pwform = PasswordChangeForm(user, request.POST)
            if pwform.is_valid():
                pwform.save()
                update_session_auth_hash(request, pwform.user)
                messages.success(request, "تم تغيير كلمة المرور.")
                return redirect("cms:profile")
    for fld in pwform.fields.values():
        fld.widget.attrs["class"] = "f-in"
    return render(request, "manage/profile.html", {"pform": pform, "pwform": pwform, "active": "profile"})


# --- inbox (contact form submissions) -----------------------------------
@staff_required
def inbox(request):
    qs = ContactMessage.objects.all()
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "manage/inbox_list.html", {
        "active": "inbox",
        "rows": page_obj,
        "page_obj": page_obj,
        "total_count": paginator.count,
        "unread_count": ContactMessage.objects.filter(is_read=False).count(),
    })


@staff_required
def inbox_detail(request, pk):
    msg = get_object_or_404(ContactMessage, pk=pk)
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "delete":
            msg.delete()
            messages.success(request, "تم حذف الرسالة.")
            return redirect("cms:inbox")
        if action == "unread":
            ContactMessage.objects.filter(pk=msg.pk).update(is_read=False)
            messages.success(request, "تم وضع علامة غير مقروءة.")
            return redirect("cms:inbox")
    if not msg.is_read:
        ContactMessage.objects.filter(pk=msg.pk).update(is_read=True)
        msg.is_read = True
    return render(request, "manage/inbox_detail.html", {"msg": msg, "active": "inbox"})


# --- dashboard ----------------------------------------------------------
@staff_required
def dashboard(request):
    pages = [
        {"label": "الصفحة الرئيسية", "desc": "الهيرو، الأرقام، القطاعات، الشركاء",
         "icon": "home", "urlname": "cms:home", "updated": HomePage.load().last_updated},
        {"label": "من نحن", "desc": "المقدمة، الأرقام، الرؤية والرسالة",
         "icon": "info", "urlname": "cms:about", "updated": AboutPage.load().last_updated},
        {"label": "الأسئلة الشائعة", "desc": "الفئات والأسئلة والأجوبة",
         "icon": "help", "urlname": "cms:faq", "updated": FaqPage.load().last_updated},
        {"label": "تواصل معنا", "desc": "القنوات، المكاتب، مواضيع النموذج",
         "icon": "phone", "urlname": "cms:contact", "updated": ContactPage.load().last_updated},
        {"label": "الشركاء", "desc": "المقدمة، التسميات، والأرقام",
         "icon": "users", "urlname": "cms:partners_page", "updated": PartnersPage.load().last_updated},
    ]
    companies = Company.objects.all()
    return render(request, "manage/dashboard.html", {
        "active": "dashboard",
        "pages": pages,
        "company_count": companies.count(),
        "companies": companies,
        "inbox_total": ContactMessage.objects.count(),
        "inbox_new": ContactMessage.objects.filter(is_read=False).count(),
        "group": Group.objects.first(),
    })


# --- home page (landing) ------------------------------------------------
@staff_required
def home_edit(request):
    page = HomePage.load()
    post = request.POST if request.method == "POST" else None
    files = request.FILES if request.method == "POST" else None

    # Section header forms all bind the same HomePage instance (disjoint fields).
    hero = F.HomeHeroForm(post, instance=page, prefix="hero")
    about = F.HomeAboutForm(post, files, instance=page, prefix="about")
    statsh = F.HomeStatsHeadForm(post, instance=page, prefix="statsh")
    subsh = F.HomeSubsHeadForm(post, instance=page, prefix="subsh")
    whyh = F.HomeWhyHeadForm(post, instance=page, prefix="whyh")
    indh = F.HomeIndHeadForm(post, instance=page, prefix="indh")
    prth = F.HomePartnersHeadForm(post, instance=page, prefix="prth")
    conh = F.HomeContactHeadForm(post, files, instance=page, prefix="conh")
    seo = F.HomeSeoForm(post, instance=page, prefix="seo")
    scalar_forms = [hero, about, statsh, subsh, whyh, indh, prth, conh, seo]

    # Repeatable card formsets.
    slides = F.HomeSlideFormSet(post, files, instance=page, prefix="slides")
    badges = F.HomeBadgeFormSet(post, instance=page, prefix="badges")
    stats = F.HomeStatFormSet(post, instance=page, prefix="stats")
    why = F.HomeWhyFormSet(post, instance=page, prefix="why")
    inds = F.HomeIndustryFormSet(post, files, instance=page, prefix="inds")
    logos = F.HomeLogoFormSet(post, files, instance=page, prefix="logos")
    citems = F.HomeContactItemFormSet(post, instance=page, prefix="citems")
    set_forms = [slides, badges, stats, why, inds, logos, citems]

    if request.method == "POST":
        forms_all = scalar_forms + set_forms
        if all(f.is_valid() for f in forms_all):
            for f in scalar_forms:
                f.save()
            for fs in set_forms:
                fs.save()
            messages.success(request, "تم حفظ الصفحة الرئيسية.")
            return redirect("cms:home")
        messages.error(request, "فيه حقول محتاجة مراجعة قبل الحفظ.")

    return render(request, "manage/home_form.html", {
        "active": "home",
        "hero": hero, "about": about, "statsh": statsh, "subsh": subsh,
        "whyh": whyh, "indh": indh, "prth": prth, "conh": conh, "seo": seo,
        "slides": slides, "badges": badges, "stats": stats, "why": why,
        "inds": inds, "logos": logos, "citems": citems,
    })


# --- group --------------------------------------------------------------
@staff_required
def group_edit(request):
    group = Group.objects.first()
    if group is None:
        group = Group.objects.create(name_ar="مجموعة APS", short="APS",
                                     phone="", email="info@aps.com.sa")
    if request.method == "POST":
        form = F.GroupForm(request.POST, request.FILES, instance=group)
        if form.is_valid():
            form.save()
            messages.success(request, "تم حفظ بيانات المجموعة.")
            return redirect("cms:group")
    else:
        form = F.GroupForm(instance=group)
    return render(request, "manage/group_form.html", {"form": form, "group": group, "active": "group"})


# --- site settings (shared texts) ---------------------------------------
@staff_required
def site_edit(request):
    site = SiteSettings.load()
    if request.method == "POST":
        form = F.SiteSettingsForm(request.POST, instance=site)
        if form.is_valid():
            form.save()
            messages.success(request, "تم حفظ إعدادات الموقع.")
            return redirect("cms:site")
    else:
        form = F.SiteSettingsForm(instance=site)
    return render(request, "manage/site_form.html", {"form": form, "active": "site"})


# --- Identity + Settings (merged: Group identity + Site settings) --------
@staff_required
def settings_edit(request):
    """One page with two tabs — group identity and shared site settings. Both
    forms share a single <form>; their field names are disjoint, and both are
    saved together."""
    group = Group.objects.first()
    if group is None:
        group = Group.objects.create(name_ar="مجموعة APS", short="APS",
                                     phone="", email="info@aps.com.sa")
    site = SiteSettings.load()
    if request.method == "POST":
        gform = F.GroupForm(request.POST, request.FILES, instance=group)
        sform = F.SiteSettingsForm(request.POST, instance=site)
        if gform.is_valid() and sform.is_valid():
            gform.save()
            sform.save()
            messages.success(request, "تم حفظ الهوية والإعدادات.")
            return redirect("cms:settings")
    else:
        gform = F.GroupForm(instance=group)
        sform = F.SiteSettingsForm(instance=site)
    return render(request, "manage/settings_form.html",
                  {"gform": gform, "sform": sform, "group": group, "active": "settings"})


# --- About page (page-as-rows; ONE form saves all sections at once) ------
@staff_required
def about_edit(request):
    page = AboutPage.load()
    GROUPS = [
        ("guiding", F.AboutGuidingHeadForm, "الرؤية والرسالة والقيم"),
        ("principles", F.AboutPrinciplesHeadForm, "مبادئ العمل"),
        ("hse", F.AboutHseHeadForm, "الصحة والسلامة والبيئة (HSE)"),
    ]

    def qs(g):
        return AboutItem.objects.filter(page=page, group=g)

    post = request.POST if request.method == "POST" else None
    files = request.FILES if request.method == "POST" else None
    intro = F.AboutIntroForm(post, files, instance=page, prefix="intro")
    facts = F.AboutFactFormSet(post, instance=page, prefix="facts")
    groups = [{"key": g, "label": lbl,
               "head": hc(post, instance=page, prefix=g + "h"),
               "items": F.AboutItemFormSet(post, files, instance=page, queryset=qs(g), prefix=g + "i")}
              for g, hc, lbl in GROUPS]

    if request.method == "POST":
        forms_all = [intro, facts] + [g["head"] for g in groups] + [g["items"] for g in groups]
        if all(f.is_valid() for f in forms_all):
            intro.save()
            facts.save()
            for g in groups:
                g["head"].save()
                objs = g["items"].save(commit=False)
                for o in objs:
                    o.group = g["key"]
                    o.save()
                for o in g["items"].deleted_objects:
                    o.delete()
            messages.success(request, "تم حفظ صفحة «من نحن».")
            return redirect("cms:about")
        messages.error(request, "فيه حقول محتاجة مراجعة قبل الحفظ.")

    return render(request, "manage/about_form.html",
                  {"intro": intro, "facts": facts, "groups": groups, "active": "about"})


@staff_required
def about_facts(request):
    page = AboutPage.load()
    if request.method == "POST":
        fs = F.AboutFactFormSet(request.POST, instance=page, prefix="items")
        if fs.is_valid():
            fs.save()
            messages.success(request, "تم حفظ الأرقام.")
            return redirect("cms:about_facts")
    else:
        fs = F.AboutFactFormSet(instance=page, prefix="items")
    return render(request, "manage/about_facts.html", {"items": fs, "active": "about"})


@staff_required
def about_items(request, group):
    page = AboutPage.load()
    labels = dict(AboutItem.GROUP_CHOICES)
    if group not in labels:
        raise Http404("Unknown group")
    qs = AboutItem.objects.filter(page=page, group=group)
    if request.method == "POST":
        fs = F.AboutItemFormSet(request.POST, instance=page, queryset=qs, prefix="items")
        if fs.is_valid():
            objs = fs.save(commit=False)
            for o in objs:
                o.group = group
                o.save()
            for o in fs.deleted_objects:
                o.delete()
            messages.success(request, "تم حفظ العناصر.")
            return redirect("cms:about_items", group=group)
    else:
        fs = F.AboutItemFormSet(instance=page, queryset=qs, prefix="items")
    return render(request, "manage/about_items.html", {
        "items": fs, "group": group, "group_label": str(labels[group]), "active": "about",
    })


# --- FAQ page -----------------------------------------------------------
@staff_required
def faq_edit(request):
    page = FaqPage.load()
    post = request.POST if request.method == "POST" else None
    files = request.FILES if request.method == "POST" else None
    form = F.FaqPageForm(post, instance=page)
    stats = F.FaqStatFormSet(post, instance=page, prefix="stats")
    cats = F.FaqCategoryEditFormSet(post, files, instance=page, prefix="cat")
    # A Q&A formset per category FORM (indexed) — covers existing categories and
    # the trailing blank "new category" block, so a category name and its
    # questions are entered and saved together in one step.
    qsets = [F.FaqItemFormSet(post, instance=cf.instance, prefix="q%d" % i)
             for i, cf in enumerate(cats.forms)]
    forms_all = [form, stats, cats] + qsets
    if request.method == "POST":
        if all(f.is_valid() for f in forms_all):
            form.save()
            stats.save()
            cats.save()  # create/update/delete categories; sets pk on each cf.instance
            deleted = set(cats.deleted_forms)
            for i, cf in enumerate(cats.forms):
                if cf in deleted or not cf.instance.pk:
                    continue  # skip deleted, and blank "new" blocks left empty
                qsets[i].instance = cf.instance
                qsets[i].save()
            messages.success(request, "تم حفظ صفحة الأسئلة الشائعة.")
            return redirect("cms:faq")
        messages.error(request, "فيه حقول محتاجة مراجعة قبل الحفظ.")
    # isnew flags the trailing blank "new category" block (extra=1, no pk yet).
    cat_blocks = [(cf, qs, not cf.instance.pk) for cf, qs in zip(cats.forms, qsets)]
    return render(request, "manage/faq_form.html", {
        "form": form, "stats": stats, "cats": cats, "cat_blocks": cat_blocks,
        "page": page, "active": "faq",
    })


@staff_required
def faq_stats(request):
    page = FaqPage.load()
    if request.method == "POST":
        fs = F.FaqStatFormSet(request.POST, instance=page, prefix="items")
        if fs.is_valid():
            fs.save()
            messages.success(request, "تم حفظ الأرقام.")
            return redirect("cms:faq_stats")
    else:
        fs = F.FaqStatFormSet(instance=page, prefix="items")
    return render(request, "manage/faq_stats.html", {"items": fs, "active": "faq"})


@staff_required
def faq_categories(request):
    page = FaqPage.load()
    if request.method == "POST":
        fs = F.FaqCategoryFormSet(request.POST, instance=page, prefix="items")
        if fs.is_valid():
            fs.save()
            messages.success(request, "تم حفظ الفئات.")
            return redirect("cms:faq_categories")
    else:
        fs = F.FaqCategoryFormSet(instance=page, prefix="items")
    return render(request, "manage/faq_categories.html", {
        "items": fs, "categories": page.categories.all(), "active": "faq",
    })


@staff_required
def faq_items(request, pk):
    category = get_object_or_404(FaqCategory, pk=pk)
    if request.method == "POST":
        fs = F.FaqItemFormSet(request.POST, instance=category, prefix="items")
        if fs.is_valid():
            fs.save()
            messages.success(request, "تم حفظ الأسئلة.")
            return redirect("cms:faq_items", pk=pk)
    else:
        fs = F.FaqItemFormSet(instance=category, prefix="items")
    return render(request, "manage/faq_items.html", {
        "items": fs, "category": category, "active": "faq",
    })


# --- Contact page -------------------------------------------------------
@staff_required
def contact_edit(request):
    page = ContactPage.load()
    post = request.POST if request.method == "POST" else None
    files = request.FILES if request.method == "POST" else None
    form = F.ContactPageForm(post, instance=page)
    channels = F.ContactChannelFormSet(post, files, instance=page, prefix="ch")
    offices = F.ContactOfficeFormSet(post, files, instance=page, prefix="off")
    forms_all = [form, channels, offices]
    if request.method == "POST":
        if all(f.is_valid() for f in forms_all):
            form.save()
            channels.save()
            offices.save()
            messages.success(request, "تم حفظ صفحة تواصل معنا.")
            return redirect("cms:contact")
        messages.error(request, "فيه حقول محتاجة مراجعة قبل الحفظ.")
    return render(request, "manage/contact_form.html", {
        "form": form, "channels": channels, "offices": offices, "active": "contact",
    })


@staff_required
def contact_channels(request):
    page = ContactPage.load()
    if request.method == "POST":
        fs = F.ContactChannelFormSet(request.POST, instance=page, prefix="items")
        if fs.is_valid():
            fs.save()
            messages.success(request, "تم حفظ قنوات التواصل.")
            return redirect("cms:contact_channels")
    else:
        fs = F.ContactChannelFormSet(instance=page, prefix="items")
    return render(request, "manage/contact_channels.html", {"items": fs, "active": "contact"})


@staff_required
def contact_offices(request):
    page = ContactPage.load()
    if request.method == "POST":
        fs = F.ContactOfficeFormSet(request.POST, instance=page, prefix="items")
        if fs.is_valid():
            fs.save()
            messages.success(request, "تم حفظ المكاتب.")
            return redirect("cms:contact_offices")
    else:
        fs = F.ContactOfficeFormSet(instance=page, prefix="items")
    return render(request, "manage/contact_offices.html", {"items": fs, "active": "contact"})


# --- Partners page ------------------------------------------------------
@staff_required
def partners_page_edit(request):
    page = PartnersPage.load()
    post = request.POST if request.method == "POST" else None
    form = F.PartnersPageForm(post, instance=page)
    facts = F.PartnersFactFormSet(post, instance=page, prefix="facts")
    if request.method == "POST":
        if form.is_valid() and facts.is_valid():
            form.save()
            facts.save()
            messages.success(request, "تم حفظ صفحة الشركاء.")
            return redirect("cms:partners_page")
        messages.error(request, "فيه حقول محتاجة مراجعة قبل الحفظ.")
    return render(request, "manage/partners_form.html",
                  {"form": form, "facts": facts, "active": "partners"})


@staff_required
def partners_facts(request):
    page = PartnersPage.load()
    if request.method == "POST":
        fs = F.PartnersFactFormSet(request.POST, instance=page, prefix="items")
        if fs.is_valid():
            fs.save()
            messages.success(request, "تم حفظ الأرقام.")
            return redirect("cms:partners_facts")
    else:
        fs = F.PartnersFactFormSet(instance=page, prefix="items")
    return render(request, "manage/partners_facts.html", {"items": fs, "active": "partners"})


# --- companies ----------------------------------------------------------
@staff_required
def company_list(request):
    return render(request, "manage/company_list.html", {
        "active": "companies",
        "companies": Company.objects.all(),
    })


def _unique_company_slug(company):
    """Auto-generate a URL slug from the company name (the slug field is no
    longer edited in the CMS). Latin name preferred; falls back to a generic
    base, then de-duplicates against existing companies."""
    base = slugify(company.name_en) or slugify(company.name_ar) or "company"
    slug, i = base, 2
    while Company.objects.filter(slug=slug).exclude(pk=company.pk).exists():
        slug = f"{base}-{i}"
        i += 1
    return slug


@staff_required
def company_add(request):
    # Step 1: create the core company record; the full sections editor opens
    # on edit (sub-sections need a saved company to attach to).
    if request.method == "POST":
        form = F.CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            company = form.save(commit=False)
            company.slug = _unique_company_slug(company)
            company.order = (Company.objects.aggregate(m=Max("order"))["m"] or 0) + 1
            company.save()
            messages.success(request, "تمت إضافة الشركة. أكمل بقية الأقسام بالأسفل.")
            return redirect("cms:company_edit", slug=company.slug)
        messages.error(request, "فيه حقول محتاجة مراجعة قبل الحفظ.")
    else:
        form = F.CompanyForm()
    return render(request, "manage/company_form.html", {
        "form": form, "company": None, "active": "companies",
    })


def _company_sections(company):
    """Get-or-create the five OneToOne sections so their formsets can bind.
    Empty auto-created sections don't render publicly (``to_context`` guards)."""
    return {
        "sys": _rel(company, "systems_section") or SystemsSection.objects.create(company=company),
        "prj": _rel(company, "projects_section") or ProjectsSection.objects.create(company=company),
        "prt": _rel(company, "partners_section") or PartnersSection.objects.create(company=company),
        "gd": _rel(company, "guiding_section") or GuidingSection.objects.create(company=company),
        "lc": _rel(company, "lifecycle_section") or LifecycleSection.objects.create(company=company),
    }


@staff_required
def company_edit(request, slug):
    company = get_object_or_404(Company, slug=slug)
    sec = _company_sections(company)
    post = request.POST if request.method == "POST" else None
    files = request.FILES if request.method == "POST" else None

    form = F.CompanyForm(post, files, instance=company)
    facts = F.FactFormSet(post, files, instance=company, prefix="facts")
    sys_form = F.SystemsSectionForm(post, files, instance=sec["sys"], prefix="sysf")
    tabs = F.TabFormSet(post, files, instance=sec["sys"], prefix="tabs")
    sys_items = F.SystemItemFormSet(post, files, instance=sec["sys"], prefix="sysi")
    prj_form = F.ProjectsSectionForm(post, files, instance=sec["prj"], prefix="prjf")
    projects = F.ProjectFormSet(post, files, instance=sec["prj"], prefix="prj")
    prt_form = F.PartnersSectionForm(post, files, instance=sec["prt"], prefix="prtf")
    logos = F.PartnerLogoFormSet(post, files, instance=sec["prt"], prefix="logos")
    gd_form = F.GuidingSectionForm(post, files, instance=sec["gd"], prefix="gdf")
    gd_items = F.GuidingItemFormSet(post, files, instance=sec["gd"], prefix="gd")
    lc_form = F.LifecycleSectionForm(post, files, instance=sec["lc"], prefix="lcf")
    phases = F.PhaseFormSet(post, files, instance=sec["lc"], prefix="ph")

    # A system item's tab must belong to THIS company's section.
    tab_qs = sec["sys"].tabs.all()
    for f in list(sys_items.forms) + [sys_items.empty_form]:
        if "tab" in f.fields:
            f.fields["tab"].queryset = tab_qs

    forms_all = [form, facts, sys_form, tabs, sys_items, prj_form, projects,
                 prt_form, logos, gd_form, gd_items, lc_form, phases]

    if request.method == "POST":
        if all(f.is_valid() for f in forms_all):
            for f in forms_all:
                f.save()
            messages.success(request, "تم حفظ بيانات الشركة.")
            return redirect("cms:company_edit", slug=form.instance.slug)
        messages.error(request, "فيه حقول محتاجة مراجعة قبل الحفظ.")

    return render(request, "manage/company_form.html", {
        "company": company, "form": form, "facts": facts,
        "sys_form": sys_form, "tabs": tabs, "sys_items": sys_items,
        "prj_form": prj_form, "projects": projects,
        "prt_form": prt_form, "logos": logos,
        "gd_form": gd_form, "gd_items": gd_items,
        "lc_form": lc_form, "phases": phases,
        "active": "companies",
    })


@staff_required
def facts_edit(request, slug):
    company = get_object_or_404(Company, slug=slug)
    if request.method == "POST":
        fs = F.FactFormSet(request.POST, instance=company, prefix="items")
        if fs.is_valid():
            fs.save()
            messages.success(request, "تم حفظ الأرقام.")
            return redirect("cms:facts_edit", slug=slug)
    else:
        fs = F.FactFormSet(instance=company, prefix="items")
    return render(request, "manage/section_facts.html", {
        "company": company, "items": fs, "active": "companies",
    })


@staff_required
def company_delete(request, slug):
    company = get_object_or_404(Company, slug=slug)
    if request.method == "POST":
        name = company.name_ar
        company.delete()
        messages.success(request, f"تم حذف الشركة: {name}.")
        return redirect("cms:companies")
    return render(request, "manage/confirm_delete.html", {
        "obj_name": company.name_ar, "back": "cms:company_edit", "slug": slug,
    })


@staff_required
def company_toggle_publish(request, slug):
    company = get_object_or_404(Company, slug=slug)
    if request.method == "POST":
        company.is_published = not company.is_published
        company.save(update_fields=["is_published"])
        messages.success(request, f"{company.name_ar}: {'نُشرت' if company.is_published else 'أُخفيت'}.")
    return redirect("cms:companies")


def _section_status(company):
    """Which optional sections a company already has (for the edit sidebar)."""
    return {
        "systems": _rel(company, "systems_section") is not None,
        "projects": _rel(company, "projects_section") is not None,
        "partners": _rel(company, "partners_section") is not None,
        "guiding": _rel(company, "guiding_section") is not None,
        "lifecycle": _rel(company, "lifecycle_section") is not None,
    }


# --- section editors ----------------------------------------------------
def _edit_section(request, slug, *, rel, model, form_cls, formsets, template, title):
    """Generic section editor: one section header form + N inline formsets.

    ``formsets`` is a list of (key, factory, prefix). Each factory is bound to
    the section instance. On POST everything is validated together and saved.
    """
    company = get_object_or_404(Company, slug=slug)
    section = _rel(company, rel)
    if section is None:
        section = model.objects.create(company=company)

    def build(data=None, files=None):
        form = form_cls(data, files, instance=section)
        fss = []
        for key, factory, prefix in formsets:
            fss.append((key, factory(data, files, instance=section, prefix=prefix)))
        return form, fss

    if request.method == "POST":
        form, fss = build(request.POST, request.FILES)
        _limit_tab_choices(fss, section)
        if form.is_valid() and all(fs.is_valid() for _, fs in fss):
            form.save()
            for _, fs in fss:
                fs.save()
            messages.success(request, f"تم حفظ قسم: {title}.")
            return redirect("cms:company_edit", slug=company.slug)
    else:
        form, fss = build()
        _limit_tab_choices(fss, section)

    ctx = {"company": company, "form": form, "section": section,
           "title": title, "active": "companies"}
    ctx.update({key: fs for key, fs in fss})
    return render(request, template, ctx)


def _limit_tab_choices(fss, section):
    """Restrict a SystemItem formset's ``tab`` choices to this section's tabs."""
    for key, fs in fss:
        if key != "items":
            continue
        for f in fs.forms:
            if "tab" in f.fields:
                f.fields["tab"].queryset = section.tabs.all()


@staff_required
def systems_edit(request, slug):
    return _edit_section(
        request, slug, rel="systems_section", model=SystemsSection,
        form_cls=F.SystemsSectionForm,
        formsets=[("tabs", F.TabFormSet, "tabs"), ("items", F.SystemItemFormSet, "items")],
        template="manage/section_systems.html", title="الأنظمة والحلول",
    )


@staff_required
def projects_edit(request, slug):
    return _edit_section(
        request, slug, rel="projects_section", model=ProjectsSection,
        form_cls=F.ProjectsSectionForm,
        formsets=[("items", F.ProjectFormSet, "items")],
        template="manage/section_projects.html", title="المشاريع",
    )


@staff_required
def project_details_edit(request, slug, pk):
    company = get_object_or_404(Company, slug=slug)
    project = get_object_or_404(Project, pk=pk, section__company=company)
    if request.method == "POST":
        fs = F.ProjectDetailFormSet(request.POST, instance=project, prefix="details")
        if fs.is_valid():
            fs.save()
            messages.success(request, "تم حفظ تفاصيل المشروع.")
            return redirect("cms:projects_edit", slug=company.slug)
    else:
        fs = F.ProjectDetailFormSet(instance=project, prefix="details")
    return render(request, "manage/section_project_details.html", {
        "company": company, "project": project, "details": fs, "active": "companies",
    })


@staff_required
def partners_edit(request, slug):
    return _edit_section(
        request, slug, rel="partners_section", model=PartnersSection,
        form_cls=F.PartnersSectionForm,
        formsets=[("logos", F.PartnerLogoFormSet, "logos")],
        template="manage/section_partners.html", title="الشركاء",
    )


@staff_required
def guiding_edit(request, slug):
    return _edit_section(
        request, slug, rel="guiding_section", model=GuidingSection,
        form_cls=F.GuidingSectionForm,
        formsets=[("items", F.GuidingItemFormSet, "items")],
        template="manage/section_guiding.html", title="المبادئ التوجيهية",
    )


@staff_required
def lifecycle_edit(request, slug):
    return _edit_section(
        request, slug, rel="lifecycle_section", model=LifecycleSection,
        form_cls=F.LifecycleSectionForm,
        formsets=[("phases", F.PhaseFormSet, "phases")],
        template="manage/section_lifecycle.html", title="دورة حياة المشروع",
    )


@staff_required
def phase_steps_edit(request, slug, pk):
    company = get_object_or_404(Company, slug=slug)
    phase = get_object_or_404(LifecyclePhase, pk=pk, section__company=company)
    if request.method == "POST":
        fs = F.StepFormSet(request.POST, instance=phase, prefix="steps")
        if fs.is_valid():
            fs.save()
            messages.success(request, "تم حفظ خطوات المرحلة.")
            return redirect("cms:lifecycle_edit", slug=company.slug)
    else:
        fs = F.StepFormSet(instance=phase, prefix="steps")
    return render(request, "manage/section_phase_steps.html", {
        "company": company, "phase": phase, "steps": fs, "active": "companies",
    })
