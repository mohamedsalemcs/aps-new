# -*- coding: utf-8 -*-
"""Home page content for the APS Group corporate website.

Copy is sourced from the client's "APS Website Content Development" sheet
(NOB's Development column) and the official company names in "APS Company
Contacts". Site language is Arabic (primary); English is provided via Django
i18n (gettext) — user-facing strings are wrapped in ``_()`` and translated in
``locale/en/LC_MESSAGES/django.po``. This module maps cleanly onto CMS models
later.
"""

from django.utils.translation import gettext_lazy as _

# --- Group identity ------------------------------------------------------
GROUP = {
    "name_ar": _("شركة التجهيزات والمشاريع العربية"),
    "name": _("شركة التجهيزات والمشاريع العربية"),
    "short": "APS",
    "phone": "+966 9200 14 515",
    "email": "info@aps.com.sa",
    "website": "aps.com.sa",
    "website_url": "https://www.aps.com.sa",
    "location_ar": _("جدة، المملكة العربية السعودية"),
}

# --- Hero slider ---------------------------------------------------------
# A light hero. Each slide varies its image layout ("cluster" = staggered
# tiles echoing the APS logo, "single" = one expressive image, "duo" = two).
HERO_CTA_PRIMARY = _("اطلب عرض سعر")
HERO_CTA_SECONDARY = _("استكشف شركات المجموعة")
HERO_BADGES = [
    {"icon": "shield", "label": _("مبني على الثقة")},
    {"icon": "handshake", "label": _("شركاء عالميون")},
    {"icon": "pin", "label": _("في كل أنحاء المملكة")},
]
HERO_SLIDES = [
    {
        "eyebrow": _("مجموعة APS الصناعية"),
        "title": _("نُمكّن الصناعة بتوريداتٍ متميّزة وتركيبٍ احترافي"),
        "subtitle": _("شركة التجهيزات والمشاريع العربية شريكك الاستراتيجي في التجارة الصناعية والتوريد المتميّز والحلول الكهروميكانيكية الاحترافية."),
        "layout": "cluster",
        "images": ["images/hero/slides/s1a.jpg", "images/hero/slides/s1b.jpg", "images/hero/slides/s1c.jpg"],
    },
    {
        "eyebrow": _("التجهيزات والمشاريع السعودية"),
        "title": _("أنظمة أمنٍ وسلامةٍ وتحكّمٍ متكاملة"),
        "subtitle": _("تكامل أنظمة الأمن والسلامة والتحكم للمنشآت الصناعية والحكومية والتجارية، من التصميم إلى التركيب والدعم."),
        "layout": "single",
        "images": ["images/hero/slides/s2.jpg"],
    },
    {
        "eyebrow": _("حلول بيتا الصناعية"),
        "title": _("آلاتٌ صناعية عالية التقنية وتركيبٌ خبير"),
        "subtitle": _("توريد وتركيب الآلات الصناعية ومعدات التصنيع، مع الدعم الفني الكامل بعد البيع في مختلف أنحاء المملكة."),
        "layout": "duo",
        "images": ["images/hero/slides/s3a.jpg", "images/hero/slides/s3b.jpg"],
    },
    {
        "eyebrow": _("الأنظمة الحديثة لتقنيات البيئة"),
        "title": _("حلول المياه والصرف والتهوية المتكاملة"),
        "subtitle": _("حلول معالجة المياه والصرف الصحي والتهوية للتطبيقات البلدية والصناعية، مع الدعم الهندسي وتسليم المشاريع المتكاملة."),
        "layout": "single",
        "images": ["images/hero/slides/s4.jpg"],
    },
    {
        "eyebrow": _("أزوليس الشرق الأوسط"),
        "title": _("طاقةٌ شمسية متكاملة للقطاع التجاري والصناعي"),
        "subtitle": _("منتجٌ مستقل للطاقة الشمسية يطوّر ويموّل ويهندس ويبني ويشغّل محطات الطاقة الشمسية للقطاع التجاري والصناعي، بأكثر من 200 مشروع عبر ثلاث قارات."),
        "layout": "cluster",
        "images": ["images/hero/slides/s5a.jpg", "images/hero/slides/s5b.jpg", "images/hero/slides/s5c.jpg"],
    },
]

# --- Stats (APS in Numbers) ---------------------------------------------
STATS_HEADING = _("APS بالأرقام")
STATS_SUBTITLE = _("كل رقم يعكس أداءً حقيقياً والتزاماً راسخاً وأثراً ملموساً.")
STATS = [
    {"value": 25, "suffix": "+", "label": _("سنة خبرة صناعية")},
    {"value": 120, "suffix": "+", "label": _("مشروع منجَز")},
    {"value": 200, "suffix": "+", "label": _("شريك ومورّد")},
    {"value": 20, "suffix": "+", "label": _("سوق عالمي")},
    {"value": 16, "suffix": "+", "label": _("قطاع نخدمه")},
    {"value": 3, "suffix": "", "label": _("مكاتب في المملكة")},
]

# --- About (APS Group at a Glance — text taken from the content sheet) ---
ABOUT = {
    "eyebrow": _("لمحة عن المجموعة"),
    "heading": _("لمحة عن مجموعة APS"),
    "paragraph": _("شركة التجهيزات والمشاريع العربية (APS) مجموعة صناعية متنوّعة تقدّم خدمات التجارة والتوريد المتميّز والتركيبات الكهروميكانيكية في مختلف أنحاء المملكة العربية السعودية، من خلال شركاتٍ متخصصة وشراكاتٍ عالمية قوية."),
    "bullets": [
        _("عمليات قائمة على النزاهة"),
        _("تحالفات دولية قوية مع الشركاء"),
        _("تغطية على مستوى المملكة، المقر الرئيسي في جدة"),
    ],
    "cta": _("اعرف المزيد"),
    "image": "images/companies/about-main.jpg",
    "image_secondary": "images/companies/about-control-room.jpg",
}

# --- What Sets APS Apart (features sourced from the sheet) ---------------
WHY_HEADING = _("ما الذي يميّز APS")
WHY_SUBTITLE = _("نقدّم حلولاً هندسية متكاملة مدعومة بعقودٍ من الخبرة، وشراكاتٍ عالمية، وأداءٍ مثبت على المدى الطويل.")
WHY = [
    {"icon": "award", "title": _("خبرة صناعية مثبتة"),
     "text": _("أكثر من عقدين من العمل الميداني في قطاعات الأمن والصناعة والبيئة.")},
    {"icon": "globe", "title": _("شراكات تقنية عالمية"),
     "text": _("نمثّل كبرى العلامات والمصنّعين العالميين لضمان الوصول إلى أحدث التقنيات.")},
    {"icon": "layers", "title": _("قدرات متكاملة عبر شركات المجموعة"),
     "text": _("حلول تمتد من التصميم والتوريد إلى التركيب والتشغيل والدعم.")},
    {"icon": "headset", "title": _("دعم ما بعد البيع"),
     "text": _("تدريب وصيانة وخدمات دعم سريعة الاستجابة بعد تسليم كل مشروع.")},
    {"icon": "shield", "title": _("الجودة والسلامة"),
     "text": _("التزام بالصحة والسلامة والبيئة وضمان الجودة في كل مرحلة من مراحل العمل.")},
    {"icon": "clock", "title": _("تسليم موثوق"),
     "text": _("تخطيط منظّم وفرق هندسية خبيرة تضمن التسليم في الوقت المحدد.")},
    {"icon": "star", "title": _("الجودة والتميّز"),
     "text": _("منتجات موثوقة ومعايير خدمة متفوّقة في كل مشروع وتعامل.")},
    {"icon": "handshake", "title": _("التزام تجاه العميل"),
     "text": _("شراكات طويلة الأمد مبنيّة على الثقة والشفافية والأداء المتّسق.")},
]

# --- Subsidiaries (Specialized Companies) --------------------------------
# Official Arabic names from the APS Company Contacts sheet. Descriptions are
# corrected to match each company's real business. SPS is listed first.
SUBS_HEADING = _("شركات متخصصة، تحت سقفٍ واحد")
SUBS_SUBTITLE = _("استكشف شركات APS في قطاعات أنظمة الأمن، والآلات الصناعية، والحلول البيئية، والتقنيات المتقدمة.")
SUBSIDIARIES = [
    {"slug": "sps", "name": _("التجهيزات والمشاريع السعودية"), "en": "Saudi Projects & Supplies",
     "sector": _("أنظمة الأمن والسلامة"),
     "desc": _("تكامل أنظمة الأمن والسلامة والتحكم للمنشآت الصناعية والحكومية والتجارية."),
     "image": "images/companies/div-security.jpg"},
    {"slug": "beta", "name": _("حلول بيتا الصناعية"), "en": "Beta Machinery",
     "sector": _("الآلات الصناعية"),
     "desc": _("توريد وتركيب الآلات الصناعية عالية التقنية، والدعم الفني بعد البيع في المملكة."),
     "image": "images/companies/div-machinery.jpg"},
    {"slug": "enviro", "name": _("الأنظمة الحديثة لتقنيات البيئة"), "en": "Envirosystems",
     "sector": _("حلول المياه والبيئة"),
     "desc": _("حلول معالجة المياه والصرف الصحي والتهوية، مع الدعم الهندسي وتسليم المشاريع المتكاملة."),
     "image": "images/companies/div-water.jpg"},
    {"slug": "ags", "name": _("الحلول الخضراء المتقدمة"), "en": "Advanced Green Solutions",
     "sector": _("الحلول الزراعية المستدامة"),
     "desc": _("حلول زراعية مستدامة وصديقة للبيئة تدعم المشاريع الخضراء والتنمية المستدامة."),
     "image": "images/companies/div-green.jpg"},
    {"slug": "azolis", "name": _("أزوليس الشرق الأوسط"), "en": "AZOLIS Middle East",
     "sector": _("الطاقة الشمسية"),
     "desc": _("منتجٌ مستقل للطاقة الشمسية يطوّر وينفّذ ويشغّل محطات الطاقة الشمسية للقطاع التجاري والصناعي عبر ثلاث قارات."),
     "image": "images/companies/div-chemicals.jpg"},
]

# --- Partners (real logos from the group's companies) --------------------
PARTNERS = {
    "eyebrow": _("شركاؤنا"),
    "heading": _("شركاء النجاح العالميون"),
    "subtitle": _("نتعاون مع كبرى المصنّعين ومزوّدي التقنية العالميين لتقديم حلول صناعية موثوقة في مختلف أنحاء المملكة."),
    "cta": _("عرض كل الشركاء"),
    "logos": [
        "images/partners/honeywell.png", "images/partners/siemens.png",
        "images/partners/cisco.png", "images/partners/hikvision.png",
        "images/partners/bose.png", "images/partners/samsung.png",
        "images/partners/lg.png", "images/partners/3m.png",
        "images/partners/nec.png", "images/partners/crestron.png",
        "images/partners/extron.png", "images/partners/avaya.png",
        "images/partners/dormakaba.png", "images/partners/fermax.png",
        "images/partners/televes.png", "images/partners/esser.png",
        "images/partners/evoqua.png",
    ],
}

# --- Industries (Industries We Power) -----------------------------------
INDUSTRIES = {
    "eyebrow": _("القطاعات"),
    "heading": _("الصناعات التي نُشغّلها"),
    "subtitle": _("حلول هندسية متكاملة مصمّمة لتشغيل البنية التحتية الحيوية، والنمو الصناعي، والبيئات الآمنة في مختلف أنحاء المملكة."),
    # "companies" tags each sector with the group subsidiary(ies) that serve it
    # (brand short-names). Mapping is grounded in each company's actual business.
    "items": [
        {"icon": "factory", "name": _("التصنيع"), "image": "images/industries/manufacturing.jpg",
         "companies": ["Beta", "SPS"],
         "desc": _("خطوط إنتاج وأنظمة أتمتة وتحكم صناعي ترفع الكفاءة وتضمن جودة التشغيل.")},
        {"icon": "drop", "name": _("المياه والصرف الصحي"), "image": "images/industries/water.jpg",
         "companies": ["Envirosystems"],
         "desc": _("حلول معالجة وضخ ومراقبة لشبكات المياه ومحطات الصرف الصحي بموثوقية عالية.")},
        {"icon": "bolt", "name": _("الطاقة والكهرباء"), "image": "images/industries/energy.jpg",
         "companies": ["AZOLIS"],
         "desc": _("أنظمة توزيع ولوحات كهربائية وحلول طاقة شمسية تدعم استمرارية الإمداد والكفاءة.")},
        {"icon": "flame", "name": _("النفط والغاز"), "image": "images/industries/oilgas.jpg",
         "companies": ["Beta"],
         "desc": _("تجهيزات ومعدات متخصصة للبيئات القاسية وفق أعلى معايير السلامة الصناعية.")},
        {"icon": "building", "name": _("البنية التحتية والإنشاءات"), "image": "images/industries/infrastructure.jpg",
         "companies": ["SPS", "Beta"],
         "desc": _("دعم متكامل لمشاريع البنية التحتية الكبرى بتوريدات وحلول هندسية موثوقة.")},
        {"icon": "health", "name": _("الرعاية الصحية"), "image": "images/industries/healthcare.jpg",
         "companies": ["SPS"],
         "desc": _("بيئات نظيفة وأنظمة تكييف وترشيح هواء متوافقة مع اشتراطات المنشآت الصحية.")},
        {"icon": "shield", "name": _("المنشآت الحكومية والأمنية"), "image": "images/industries/government.jpg",
         "companies": ["SPS"],
         "desc": _("أنظمة أمنية ومراقبة وتحكم متكاملة تلبّي متطلبات المنشآت الحساسة.")},
        {"icon": "shop", "name": _("المباني التجارية والضيافة"), "image": "images/industries/commercial.jpg",
         "companies": ["SPS"],
         "desc": _("حلول كهروميكانيكية وأنظمة مباني ذكية ترفع الراحة وكفاءة التشغيل.")},
        {"icon": "leaf", "name": _("الزراعة والاستدامة"), "image": "images/industries/agriculture.jpg",
         "companies": ["AGS"],
         "desc": _("حلول زراعية مستدامة ومنتجات حماية ومغذّيات نباتية ترفع الإنتاجية وتحافظ على البيئة.")},
    ],
}

# --- Contact (home shows only phone / email / location) ------------------
CONTACT = {
    "eyebrow": _("تواصل معنا"),
    "heading": _("فريقنا في خدمتك"),
    "subtitle": _("يستجيب فريقنا بدعمٍ سريعٍ وموثوق، مصمَّم خصيصاً لاحتياجاتك الصناعية والكهروميكانيكية."),
    "image": "images/hero/contact-industrial.jpg",
    "items": [
        {"icon": "phone", "label": _("اتصل بنا"), "value": "+966 9200 14 515", "href": "tel:+966920014515", "ltr": True},
        {"icon": "mail", "label": _("راسلنا"), "value": "info@aps.com.sa", "href": "mailto:info@aps.com.sa", "ltr": True},
        {"icon": "pin", "label": _("موقعنا"), "value": _("جدة، المملكة العربية السعودية"), "href": "", "ltr": False},
    ],
}

# --- Navigation ----------------------------------------------------------
# "Contact" is intentionally NOT a nav item: its page (/contact/) is reached
# via the approved header CTA button, so we don't duplicate it as a nav link.
# Nav links point to real pages — "Partners" goes to its /partners/ page, NOT a
# #partners jump to the home section.
NAV = [
    {"label": _("الرئيسية"), "href": "/"},
    {"label": _("من نحن"), "href": "/about/"},
    {"label": _("شركات المجموعة"), "href": "/#subsidiaries", "dropdown": True},
    {"label": _("الشركاء"), "href": "/partners/"},
    {"label": _("الأسئلة الشائعة"), "href": "/faq/"},
]


# --- SEO -----------------------------------------------------------------
# Site-wide fallback (exposed to every page via the site_globals processor)
# and per-page overrides. Images are static paths; the template resolves them
# to absolute URLs for Open Graph / Twitter cards.
SEO_DEFAULTS = {
    "title": _("مجموعة APS | شركة التجهيزات والمشاريع العربية"),
    "description": _(
        "مجموعة APS الصناعية: التجارة والتوريد المتميّز والحلول الكهروميكانيكية "
        "المتخصصة عبر شركاتٍ متخصصة وشراكاتٍ عالمية في مختلف أنحاء المملكة العربية السعودية."
    ),
    "image": "images/hero/hero-industrial.jpg",
    "type": "website",
}

HOME_SEO = {
    "title": _("مجموعة APS | حلول صناعية وكهروميكانيكية وتوريدات متميّزة في السعودية"),
    "description": _(
        "شركة التجهيزات والمشاريع العربية (APS): مجموعة صناعية سعودية تقدّم التوريد "
        "المتميّز والحلول الكهروميكانيكية وأنظمة الأمن والمياه عبر شركاتٍ متخصصة "
        "وشراكاتٍ عالمية في مختلف أنحاء المملكة."
    ),
    "image": "images/hero/hero-industrial.jpg",
    "type": "website",
}


def home_context():
    return {
        "seo": HOME_SEO,
        "group": GROUP,
        "nav": NAV,
        "hero_slides": HERO_SLIDES,
        "hero_badges": HERO_BADGES,
        "hero_cta_primary": HERO_CTA_PRIMARY,
        "hero_cta_secondary": HERO_CTA_SECONDARY,
        "stats_heading": STATS_HEADING,
        "stats_subtitle": STATS_SUBTITLE,
        "stats": STATS,
        "about": ABOUT,
        "why_heading": WHY_HEADING,
        "why_subtitle": WHY_SUBTITLE,
        "why": WHY,
        "subs_heading": SUBS_HEADING,
        "subs_subtitle": SUBS_SUBTITLE,
        "subsidiaries": SUBSIDIARIES,
        "partners": PARTNERS,
        "industries": INDUSTRIES,
        "contact": CONTACT,
    }
