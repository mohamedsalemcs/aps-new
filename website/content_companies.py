# -*- coding: utf-8 -*-
"""Per-company (subsidiary) page content. Each company has its own identity,
contacts, partners, and a different mix of sections. Content and assets are
sourced from each company's own website + the "APS Website Content Development"
sheet.

User-facing strings are wrapped in ``_()`` (gettext); English lives in
``locale/en/LC_MESSAGES/django.po``. Slugs, logos, image paths, phones,
emails, URLs, map queries and technical power ratings are NOT translated.
"""

from django.utils.translation import gettext_lazy as _

# All SPS partner logos (from spsc.com.sa) — named brands + numbered vendors.
SPS_PARTNERS = [
    "aletron", "honeywell-sec", "esser", "ex-or", "televes", "austco", "paso",
    "mobatime", "avaya", "hp", "keytop", "cisco", "siemens", "systimax", "3m",
    "dat", "wavetech", "vesda", "phonex-control", "fermax", "hikvision",
    "samsung", "lg", "qsc", "da-lite", "bose", "blamp", "extron", "cg",
    "honeywell", "nec", "absen", "dormakaba", "crestron",
] + ["vendors-%d" % i for i in range(1, 21)]

COMPANIES = {
    "sps": {
        "slug": "sps",
        "name": _("التجهيزات والمشاريع السعودية"),
        "en": "Saudi Projects & Supplies",
        "eyebrow": _("شركة تابعة لمجموعة APS"),
        "sector": _("أنظمة الأمن والسلامة والتحكم"),
        "logo": "logos/sps-logo.png",
        "hero_image": "images/companies/div-security.jpg",
        "breadcrumb": [
            {"label": _("الرئيسية"), "href": "/"},
            {"label": _("شركات المجموعة"), "href": "/#subsidiaries"},
            {"label": _("التجهيزات والمشاريع السعودية")},
        ],
        "intro_lead": _(
            "شركة التجهيزات والمشاريع السعودية (SPS) مزوّدٌ رائد لأنظمة الأمن والسلامة "
            "والتحكم المتكاملة، تخدم المنشآت الصناعية والحكومية والسكنية والصحية "
            "والتعليمية في مختلف أنحاء المملكة، وتقدّم حلولاً متكاملة من تصميم الأنظمة "
            "وتركيبها إلى التدريب والدعم بعد البيع عبر مكاتبها."
        ),
        "facts": [
            {"value": "2001", "suffix": "", "label": _("سنة التأسيس")},
            {"value": "3", "suffix": "", "label": _("مكاتب في المملكة")},
            {"value": "5", "suffix": "", "label": _("مجالات أنظمة")},
            {"value": "20", "suffix": "+", "label": _("سنة خبرة")},
        ],

        "about": {
            "eyebrow": _("عن الشركة"),
            "heading": _("خبرةٌ تمتد منذ عام 2001"),
            "paragraph": _(
                "تأسّست SPS عام 2001 كمزوّدٍ لأنظمة الأمن والسلامة والتحكم المتكاملة عبر "
                "المملكة، وتخدم القطاعات الصناعية والحكومية والسكنية والصحية والتعليمية "
                "بحلولٍ متقدّمة مصمّمة وفق الاحتياجات التشغيلية المتنوّعة. تعمل الشركة على "
                "مستوى المملكة بسمعةٍ قوية في الجودة والموثوقية، ويُنفَّذ كل مشروع بدقةٍ "
                "واحترافية لضمان أداءٍ طويل الأمد. ويُمكّن الاستثمار المستمر في الكفاءات "
                "والتقنيات SPS من أن تبقى شريكاً استشرافياً قائماً على الحلول."
            ),
            "bullets": [],
        },

        # 5 categories (tabs), each with its products — mirrors spsc.com.sa.
        "systems": {
            "eyebrow": _("الأنظمة والحلول"),
            "heading": _("أنظمة السلامة والأمن والتحكم"),
            "subtitle": _("محفظةٌ متكاملة من الأنظمة موزّعة على خمس فئات رئيسية، مصمّمة لتعزيز السلامة والكفاءة التشغيلية وإدارة المنشآت."),
            "tabs": [
                {"icon": "flame", "title": _("أنظمة السلامة الحياتية"), "items": [
                    {"name": _("نظام كشف الحرائق والإنذار"), "image": "images/companies/sps/systems/fire-alarm.jpg"},
                    {"name": _("نظام الإخلاء الصوتي"), "image": "images/companies/sps/systems/voice-evacuation.jpg"},
                    {"name": _("نظام الشفط للإنذار المبكر"), "image": "images/companies/sps/systems/aspiration.jpg"},
                ]},
                {"icon": "shield", "title": _("أنظمة الأمن"), "items": [
                    {"name": _("أنظمة المراقبة بالكاميرات (CCTV)"), "image": "images/companies/sps/systems/cctv.jpg"},
                    {"name": _("أنظمة التحكم في الدخول"), "image": "images/companies/sps/systems/access-control.jpg"},
                    {"name": _("أنظمة إنذار التسلل"), "image": "images/companies/sps/systems/intrusion.jpg"},
                    {"name": _("أنظمة أقفال الأبواب"), "image": "images/companies/sps/systems/door-locking.jpg"},
                ]},
                {"icon": "layers", "title": _("أنظمة التحكم"), "items": [
                    {"name": _("نظام إدارة المباني (BMS)"), "image": "images/companies/sps/systems/bms.jpg"},
                    {"name": _("أنظمة التحكم بالإضاءة"), "image": "images/companies/sps/systems/lighting.jpg"},
                    {"name": _("أنظمة غرف العزل"), "image": "images/companies/sps/systems/isolation.jpg"},
                    {"name": _("حلول الطاقة غير المنقطعة (UPS)"), "image": "images/companies/sps/systems/ups.jpg"},
                    {"name": _("نظام إدارة مواقف السيارات"), "image": "images/companies/sps/systems/car-parking.jpg"},
                ]},
                {"icon": "globe", "title": _("أنظمة الضيافة والشبكات والإدارة"), "items": [
                    {"name": _("نظام النداء الصوتي العام"), "image": "images/companies/sps/systems/public-address.jpg"},
                    {"name": _("نظام الساعة المركزية"), "image": "images/companies/sps/systems/master-clock.jpg"},
                    {"name": _("نظام استدعاء الممرّضات"), "image": "images/companies/sps/systems/nurse-call.jpg"},
                    {"name": _("أنظمة MATV و IPTV و GPON"), "image": "images/companies/sps/systems/matv.jpg"},
                    {"name": _("حلول شبكات البيانات"), "image": "images/companies/sps/systems/data-network.jpg"},
                    {"name": _("نظام الهاتف عبر الإنترنت (VOIP)"), "image": "images/companies/sps/systems/voip.jpg"},
                    {"name": _("نظام الاتصال الداخلي"), "image": "images/companies/sps/systems/intercom.jpg"},
                    {"name": _("نظام إدارة غرف الضيوف (GRMS)"), "image": "images/companies/sps/systems/grms.jpg"},
                    {"name": _("أنظمة إدارة الطوابير الرقمية"), "image": "images/companies/sps/systems/queuing.jpg"},
                ]},
                {"icon": "headset", "title": _("الأنظمة السمعية والبصرية"), "items": [
                    {"name": _("أنظمة الصوت والفيديو"), "image": "images/companies/sps/systems/audio-video.jpg"},
                    {"name": _("نظام الموسيقى الخلفية"), "image": "images/companies/sps/systems/background-music.jpg"},
                    {"name": _("نظام اللافتات الرقمية"), "image": "images/companies/sps/systems/digital-signage.jpg"},
                    {"name": _("أنظمة إضاءة المسرح"), "image": "images/companies/sps/systems/stage-lights.jpg"},
                ]},
            ],
        },

        "projects": {
            "eyebrow": _("مشاريعنا"),
            "heading": _("مشاريع نفّذتها SPS"),
            "subtitle": _("مجموعة مختارة من المشاريع التي نفّذتها الشركة في مختلف أنحاء المملكة."),
            "items": [
                {"name": _("مركز الملك عبدالله المالي (كافد)"), "sector": _("حكومي"), "image": "images/companies/sps/projects/kafd.jpg"},
                {"name": _("جامعة الملك عبدالله للعلوم والتقنية"), "sector": _("تعليمي"), "image": "images/companies/sps/projects/kaust.jpg"},
                {"name": _("جامعة الملك سعود"), "sector": _("تعليمي"), "image": "images/companies/sps/projects/ksu.jpg"},
                {"name": _("مستشفى الملك فهد"), "sector": _("صحي"), "image": "images/companies/sps/projects/king-fahad-hospital.jpg"},
                {"name": _("الهيئة العامة للغذاء والدواء"), "sector": _("حكومي"), "image": "images/companies/sps/projects/sfda.jpg"},
                {"name": _("واجهة أجدان البحرية"), "sector": _("تجاري"), "image": "images/companies/sps/projects/ajdan-waterfront.jpg"},
                {"name": _("مبنى الغرفة التجارية"), "sector": _("تجاري"), "image": "images/companies/sps/projects/chamber-khobar.jpg"},
                {"name": _("نورث بيتش، الجبيل"), "sector": _("ضيافة"), "image": "images/companies/sps/projects/north-beach.jpg"},
            ],
        },

        "partners": {
            "eyebrow": _("شركاؤنا"),
            "heading": _("شركاء التقنية العالميون"),
            "subtitle": _("نمثّل نخبةً من كبرى المصنّعين العالميين لأنظمة الأمن والسلامة والتحكم والأنظمة السمعية والبصرية."),
            "logos": ["images/companies/sps/partners/%s.png" % p for p in SPS_PARTNERS],
        },

        "contact": {
            "phone": "+966 9200 14 515",
            "email": "sales.sps@aps.com.sa",
            "website": "spsc.com.sa",
            "website_url": "https://www.spsc.com.sa",
            "offices": [_("جدة (المقر الرئيسي)"), _("الرياض"), _("الخبر")],
        },
    },

    # ================= Beta Machinery (beta-machinery.net) =================
    "beta": {
        "slug": "beta",
        "name": _("حلول بيتا الصناعية"),
        "en": "Beta Machinery",
        "eyebrow": _("شركة تابعة لمجموعة APS"),
        "sector": _("الآلات الصناعية والمعدات"),
        "logo": "logos/beta-logo.png",
        "hero_image": "images/companies/div-machinery.jpg",
        "hero_cta": _("استكشف الآلات"),
        "breadcrumb": [
            {"label": _("الرئيسية"), "href": "/"},
            {"label": _("شركات المجموعة"), "href": "/#subsidiaries"},
            {"label": _("حلول بيتا الصناعية")},
        ],
        "about": {
            "paragraph": _(
                "حلول بيتا الصناعية، التي تأسّست عام 1996، شركة متخصصة تابعة لمجموعة APS "
                "تُعنى بتوفير حلول الآلات الصناعية عالية التقنية في مختلف أنحاء المملكة. "
                "ندعم العمليات الصناعية بحلولٍ متكاملة، من توريد المعدات وتركيبها إلى "
                "التشغيل، مصمّمة وفق المتطلبات التشغيلية لضمان أداءٍ طويل الأمد. ويقدّم "
                "فريقنا الهندسي تركيبات خطوط إنتاج كاملة مدعومة بالتدريب والخبرة الفنية المستمرة."
            ),
            "bullets": [
                _("تأسّست عام 1996"),
                _("دعم صناعي على مستوى المملكة"),
                _("حلول آلات متقدمة وتدريب فني"),
            ],
        },
        "facts": [
            {"value": "1996", "suffix": "", "label": _("سنة التأسيس")},
            {"value": "30", "suffix": "+", "label": _("سنة خبرة")},
            {"value": "42", "suffix": "", "label": _("آلة ومعدة")},
            {"value": "24", "suffix": "", "label": _("فئة منتجات")},
        ],

        # 2 categories (tabs), each item = machine name + image (from beta-machinery.net)
        "systems": {
            "eyebrow": _("الآلات والمعدات"),
            "heading": _("فئات الآلات والأدوات الصناعية"),
            "subtitle": _("تشكيلة واسعة من الآلات الصناعية عالية التقنية والأدوات والمستهلكات لدعم عمليات التصنيع في مختلف القطاعات."),
            "tabs": [
                {"icon": "factory", "title": _("الآلات"), "items": [
                    {"name": _("معالجة البروفايل الألمنيوم"), "image": "images/companies/beta/machines/aluminum-profile.jpg"},
                    {"name": _("المناشير الشريطية"), "image": "images/companies/beta/machines/band-saw.jpg"},
                    {"name": _("آلات معالجة قضبان التوصيل"), "image": "images/companies/beta/machines/busbar.jpg"},
                    {"name": _("آلات التخريم CNC"), "image": "images/companies/beta/machines/cnc-punching.jpg"},
                    {"name": _("ليزر CO2"), "image": "images/companies/beta/machines/co2-laser.jpg"},
                    {"name": _("قص وتخديد الألواح المركبة"), "image": "images/companies/beta/machines/composite-panel.jpg"},
                    {"name": _("القص بليزر الفايبر"), "image": "images/companies/beta/machines/fiber-laser.jpg"},
                    {"name": _("آلات حقن الفوم"), "image": "images/companies/beta/machines/foam-injection.jpg"},
                    {"name": _("آلات الطي"), "image": "images/companies/beta/machines/folding.jpg"},
                    {"name": _("المكابس الساخنة والباردة"), "image": "images/companies/beta/machines/hot-cold-press.jpg"},
                    {"name": _("آلة تشكيل الحديد"), "image": "images/companies/beta/machines/iron-worker.jpg"},
                    {"name": _("اللحام بالليزر"), "image": "images/companies/beta/machines/laser-welding.jpg"},
                    {"name": _("القص بالبلازما"), "image": "images/companies/beta/machines/plasma-cutting.jpg"},
                    {"name": _("آلات ثني الألواح والبروفايل"), "image": "images/companies/beta/machines/plate-bending.jpg"},
                    {"name": _("مكابس الثني"), "image": "images/companies/beta/machines/press-brake.jpg"},
                    {"name": _("الحلول الروبوتية"), "image": "images/companies/beta/machines/robotic.jpg"},
                    {"name": _("آلة التخديد V"), "image": "images/companies/beta/machines/v-grooving.jpg"},
                    {"name": _("آلات الأخشاب"), "image": "images/companies/beta/machines/wood.jpg"},
                ]},
                {"icon": "shop", "title": _("الأدوات والمستهلكات"), "items": [
                    {"name": _("أقراص الجلخ"), "image": "images/companies/beta/machines/grinding-discs.jpg"},
                    {"name": _("مستهلكات الليزر والبلازما"), "image": "images/companies/beta/machines/laser-plasma-consumables.jpg"},
                    {"name": _("أدوات الخراطة والتفريز"), "image": "images/companies/beta/machines/lathe-milling.jpg"},
                    {"name": _("أدوات مكابس الثني"), "image": "images/companies/beta/machines/press-brake-tools.jpg"},
                    {"name": _("أدوات التخريم"), "image": "images/companies/beta/machines/punching-tools.jpg"},
                    {"name": _("مستهلكات اللحام"), "image": "images/companies/beta/machines/welding-consumables.jpg"},
                ]},
            ],
        },

        "partners": {
            "eyebrow": _("شركاؤنا"),
            "heading": _("علاماتٌ عالمية نمثّلها"),
            "subtitle": _("نمثّل نخبةً من كبرى مصنّعي الآلات والمعدات الصناعية حول العالم."),
            "logos": [
                "images/companies/beta/partners/bodor.png",
                "images/companies/beta/partners/lvd-hd.png",
                "images/companies/beta/partners/ysd.png",
                "images/companies/beta/partners/seco.png",
                "images/companies/beta/partners/steeltailor.png",
                "images/companies/beta/partners/thermacut.png",
            ],
        },

        "contact": {
            "phone": "+966 11 242 8467",
            "email": "sales@betamachinery.com.sa",
            "website": "beta-machinery.net",
            "website_url": "https://beta-machinery.net",
            "offices": [_("جدة (المقر الرئيسي)"), _("الرياض"), _("الخبر")],
        },
    },

    # ============= Envirosystems (envirosystems.com.sa) =============
    "enviro": {
        "slug": "enviro",
        "name": _("الأنظمة الحديثة لتقنيات البيئة"),
        "en": "Envirosystems",
        "eyebrow": _("شركة تابعة لمجموعة APS"),
        "sector": _("حلول المياه والصرف الصحي والتهوية"),
        "logo": "logos/enviro-logo.png",
        "hero_image": "images/companies/div-water.jpg",
        "hero_cta": _("استكشف الحلول"),
        "breadcrumb": [
            {"label": _("الرئيسية"), "href": "/"},
            {"label": _("شركات المجموعة"), "href": "/#subsidiaries"},
            {"label": _("الأنظمة الحديثة لتقنيات البيئة")},
        ],
        "about": {
            "paragraph": _(
                "تأسّست شركة الأنظمة الحديثة لتقنيات البيئة عام 2000، وهي مزوّدٌ ومقدّم "
                "خدمات رائد لقطاعات المياه والصرف الصحي والتهوية في المملكة. من خلال "
                "شراكاتٍ مع كبرى المصنّعين العالميين، توفّر الشركة حلولاً متقدمة وفعّالة "
                "من حيث التكلفة للتطبيقات البلدية والصناعية، وتدعم المشاريع من التقييم "
                "الأولي إلى التنفيذ المتكامل، بقدراتٍ هندسية قوية تشمل التصميم والهندسة "
                "الميكانيكية والكهربائية."
            ),
            "bullets": [
                _("تأسّست عام 2000"),
                _("شراكات مع مصنّعين عالميين"),
                _("حلول للتطبيقات البلدية والصناعية"),
            ],
        },
        "facts": [
            {"value": "2000", "suffix": "", "label": _("سنة التأسيس")},
            {"value": "25", "suffix": "+", "label": _("سنة خبرة")},
            {"value": "6", "suffix": "", "label": _("حلول رئيسية")},
            {"value": "11", "suffix": "+", "label": _("مشروع منجَز")},
        ],

        # Products/solutions as a plain grid (image + name) — from the site.
        "systems": {
            "eyebrow": _("المنتجات والحلول"),
            "heading": _("حلول المياه والبيئة"),
            "subtitle": _("مجموعة متكاملة من حلول ومنتجات معالجة المياه والصرف الصحي والتهوية للتطبيقات البلدية والصناعية."),
            "items": [
                {"name": _("تعقيم المياه"), "image": "images/companies/enviro/products/water-disinfection.jpg"},
                {"name": _("ترشيح المياه"), "image": "images/companies/enviro/products/water-filtration.jpg"},
                {"name": _("ضخ المياه"), "image": "images/companies/enviro/products/water-pumping.jpg"},
                {"name": _("الجرعات الكيميائية"), "image": "images/companies/enviro/products/chemical-dosing.jpg"},
                {"name": _("التحكم في الروائح"), "image": "images/companies/enviro/products/odor-control.jpg"},
                {"name": _("التهوية"), "image": "images/companies/enviro/products/ventilation.jpg"},
            ],
        },

        "projects": {
            "eyebrow": _("مشاريعنا"),
            "heading": _("مشاريع نفّذتها الشركة"),
            "subtitle": _("مجموعة من كبرى مشاريع المياه والبنية التحتية البيئية في مختلف أنحاء المملكة."),
            "items": [
                {"name": _("نظام التوليد الموقعي للكلور (OSEC)"), "image": "images/companies/enviro/projects/alhasa-osec.jpg"},
                {"name": _("نظام ثاني أكسيد الكلور"), "image": "images/companies/enviro/projects/qunfudhah-clo2.jpg"},
                {"name": _("أنظمة الترشيح الحيوي للتحكم في الروائح"), "image": "images/companies/enviro/projects/dammam-khobar-ltom.jpg"},
                {"name": _("الخزان الاستراتيجي بمكة المكرمة"), "image": "images/companies/enviro/projects/makkah-reservoir.jpg"},
                {"name": _("مدينة جازان الاقتصادية"), "image": "images/companies/enviro/projects/jazan-economic.jpg"},
                {"name": _("الخزان الاستراتيجي (مليون م³) بالرياض"), "image": "images/companies/enviro/projects/riyadh-reservoir.jpg"},
                {"name": _("محطات رفع جازان (عقد 1 و2)"), "image": "images/companies/enviro/projects/jazan-lift.jpg"},
                {"name": _("محطات رفع ينبع"), "image": "images/companies/enviro/projects/yanbu-lift.jpg"},
                {"name": _("محطة معالجة الحاير"), "image": "images/companies/enviro/projects/alhayer-stp.jpg"},
                {"name": _("الخزانات الاستراتيجية (1.5 مليون م³) بجدة"), "image": "images/companies/enviro/projects/jeddah-reservoirs.jpg"},
                {"name": _("خط نقل مياه الشعيبة"), "image": "images/companies/enviro/projects/shoaiba-line.jpg"},
                {"name": _("محطة معالجة الجبيل EPC"), "image": "images/companies/enviro/projects/jubail-stp.jpg"},
            ],
        },

        "partners": {
            "eyebrow": _("الموردون الدوليون"),
            "heading": _("شركاؤنا من المصنّعين العالميين"),
            "subtitle": _("نمثّل نخبةً من كبرى المصنّعين العالميين في تقنيات المياه والبيئة."),
            "logos": [
                "images/companies/enviro/partners/grundfos.png",
                "images/companies/enviro/partners/evoqua.png",
                "images/companies/enviro/partners/sodeca.png",
                "images/companies/enviro/partners/itc.png",
                "images/companies/enviro/partners/halogen.png",
                "images/companies/enviro/partners/forceflow.png",
                "images/companies/enviro/partners/denora.png",
            ],
        },

        "contact": {
            "phone": "+966 12 661 7470",
            "email": "info@envirosystems.com.sa",
            "website": "envirosystems.com.sa",
            "website_url": "https://envirosystems.com.sa",
            "offices": [_("جدة (المقر الرئيسي)")],
        },
    },

    # ============= Advanced Green Solutions (ags-ae.com, Dubai) =============
    "ags": {
        "slug": "ags",
        "name": _("الحلول الخضراء المتقدمة"),
        "en": "Advanced Green Solutions",
        "eyebrow": _("شركة تابعة لمجموعة APS"),
        "sector": _("الحلول الزراعية المستدامة"),
        "logo": "logos/ags-logo.png",
        "hero_image": "images/companies/div-green.jpg",
        "hero_cta": _("استكشف المنتجات"),
        "breadcrumb": [
            {"label": _("الرئيسية"), "href": "/"},
            {"label": _("شركات المجموعة"), "href": "/#subsidiaries"},
            {"label": _("الحلول الخضراء المتقدمة")},
        ],
        "about": {
            "paragraph": _(
                "الحلول الخضراء المتقدمة شركة مقرها دبي تقدّم حلولاً عملية ومستدامة "
                "للزراعة والعناية بالمسطحات الخضراء. مبنيّةً على خبرةٍ في المجال، نعمل "
                "عن قربٍ مع عملائنا لمعالجة تحديات الحقل الحقيقية، بما يعزّز أداء المحاصيل "
                "ويحسّن صحة النبات ويدعم الإنتاجية طويلة الأمد من خلال حلولٍ ومنتجاتٍ "
                "وإرشادٍ فني مصمّم وفق الاحتياجات."
            ),
            "bullets": [
                _("مقرها دبي، الإمارات العربية المتحدة"),
                _("منتجات صديقة للبيئة"),
                _("خبرة في علم الزراعة والعناية بالنبات"),
            ],
        },
        "facts": [
            {"value": "8", "suffix": "", "label": _("فئات منتجات")},
            {"value": "13", "suffix": "+", "label": _("نوع منتج")},
            {"value": "2", "suffix": "", "label": _("قطاعان نخدمهما")},
            {"value": "100", "suffix": "%", "label": _("حلول مستدامة")},
        ],

        # Our Guiding Principles (Vision + Mission)
        "guiding": {
            "eyebrow": _("مبادئنا التوجيهية"),
            "heading": _("الرؤية والرسالة"),
            "items": [
                {"icon": "eye", "title": _("الرؤية"),
                 "text": _("أن نكون مزوّداً رائداً لحلول علم الزراعة ومساهماً رئيسياً في منتجات صحة النبات الصديقة للبيئة، بما يدفع الزراعة المستدامة في المنطقة وخارجها.")},
                {"icon": "target", "title": _("الرسالة"),
                 "text": _("تقديم حلولٍ زراعية فعّالة تعزّز صحة المحاصيل وتحسّن الإنتاجية وتدعم الاستدامة طويلة الأمد، محقّقةً نتائج ملموسة لكل عملية زراعية.")},
            ],
        },

        # Product range (image + name, plain grid) — categories from ags-ae.com.
        "systems": {
            "eyebrow": _("منتجاتنا"),
            "heading": _("مجموعة المنتجات"),
            "subtitle": _("تشكيلة واسعة من منتجات علم الزراعة عالية الجودة لتلبية احتياجات المحاصيل عبر الموسم."),
            "items": [
                {"name": _("الأسمدة المفردة"), "image": "images/companies/ags/products/straight-fertilizers.jpg"},
                {"name": _("الأسمدة الذائبة في الماء"), "image": "images/companies/ags/products/water-soluble.jpg"},
                {"name": _("الأسمدة الحبيبية"), "image": "images/companies/ags/products/granular.jpg"},
                {"name": _("المبيدات"), "image": "images/companies/ags/products/pesticides.jpg"},
                {"name": _("المنشّطات الحيوية والأسمدة السائلة"), "image": "images/companies/ags/products/bio-stimulants.jpg"},
                {"name": _("محسّنات التربة"), "image": "images/companies/ags/products/soil-conditioners.jpg"},
                {"name": _("مساعدات الرش والمنتجات المتخصصة"), "image": "images/companies/ags/products/adjuvants.jpg"},
                {"name": _("البذور"), "image": "images/companies/ags/products/seeds.jpg"},
            ],
        },

        "contact": {
            "phone": "+971 4 354 1872",
            "email": "ags@ags-ae.com",
            "website": "ags-ae.com",
            "website_url": "https://www.ags-ae.com",
            "offices": [_("دبي، الإمارات العربية المتحدة")],
        },
    },

    # ================= AZOLIS Middle East (azolis.com — solar) =================
    "azolis": {
        "slug": "azolis",
        "name": _("أزوليس الشرق الأوسط"),
        "en": "AZOLIS Middle East",
        "eyebrow": _("شركة تابعة لمجموعة APS"),
        "sector": _("حلول الطاقة الشمسية"),
        "logo": "logos/azolis-logo.png",
        "hero_image": "images/companies/div-chemicals.jpg",
        "hero_cta": _("استكشف المشاريع"),
        "hero_cta_href": "#projects",
        "breadcrumb": [
            {"label": _("الرئيسية"), "href": "/"},
            {"label": _("شركات المجموعة"), "href": "/#subsidiaries"},
            {"label": _("أزوليس الشرق الأوسط")},
        ],
        "about": {
            "paragraph": _(
                "أزوليس منتِجٌ مستقل للطاقة الشمسية، متخصص في تطوير وتمويل وهندسة وإنشاء "
                "وصيانة محطات الطاقة الكهروضوئية لقطاع الشركات والصناعة (C&I). أنجزت "
                "الشركة أكثر من 200 مشروع عبر ثلاث قارات، ولها مكاتب في فرنسا والمغرب، "
                "بخبرةٍ تمتد إلى المشاريع متوسطة الحجم حتى 5 ميجاوات."
            ),
            "bullets": [
                _("منتِج مستقل للطاقة الشمسية"),
                _("تطوير وتمويل وهندسة وإنشاء وصيانة"),
                _("مكاتب في فرنسا والمغرب"),
            ],
        },
        "facts": [
            {"value": "200", "suffix": "+", "label": _("مشروع منجَز")},
            {"value": "3", "suffix": "", "label": _("قارات")},
            {"value": "2", "suffix": "", "label": _("مكاتب دولية")},
            {"value": "2014", "suffix": "", "label": _("سنة التأسيس")},
        ],

        # Solar project lifecycle (2 phases × 5 steps) — from the AZOLIS sheet.
        "lifecycle": {
            "eyebrow": _("دورة حياة المشروع"),
            "heading": _("دورة حياة مشروع الطاقة الشمسية"),
            "subtitle": _("نُدير كل مرحلة من مراحل مشروع الطاقة الشمسية بدقةٍ وخبرة، من التطوير المبكّر إلى التشغيل والصيانة طويلة الأمد."),
            "phases": [
                {"no": "01", "title": _("تطوير المشروع"), "steps": [
                    {"title": _("ما قبل التطوير"), "text": _("تقييم الموقع ودراسات الجدوى وتقييم الموارد والفحص الفني الأولي.")},
                    {"title": _("التصاريح الإدارية"), "text": _("التصاريح وتقييمات الأثر البيئي وحقوق الأرض والموافقات التنظيمية.")},
                    {"title": _("عقد ربط الشبكة"), "text": _("الدراسات الفنية والاتفاقيات الرسمية مع مشغّل الشبكة للربط الكهربائي.")},
                    {"title": _("التعاقد مع العميل"), "text": _("اتفاقيات شراء الطاقة واتفاقيات الشراء والتفاوض على الشروط التجارية.")},
                    {"title": _("التمويل"), "text": _("تأمين تمويل المشروع وهيكلة رأس المال وتنسيق الإغلاق المالي.")},
                ]},
                {"no": "02", "title": _("الإنشاء والتشغيل والصيانة"), "steps": [
                    {"title": _("هندسة المشروع"), "text": _("التصميم الكهربائي والمدني والإنشائي التفصيلي وتحسين التخطيط.")},
                    {"title": _("مسح الموقع"), "text": _("المسوحات الطبوغرافية والتحقيقات الجيوتقنية وتقييم الموقع الميداني.")},
                    {"title": _("الإنشاء"), "text": _("الأعمال المدنية وأنظمة التركيب وتركيب الألواح والكابلات وبناء المحطة الفرعية.")},
                    {"title": _("التشغيل التجريبي"), "text": _("الاختبار والتحقق من الأداء ومزامنة الشبكة والتسليم للتشغيل.")},
                    {"title": _("التشغيل والصيانة"), "text": _("إدارة الأصول طويلة الأمد ومراقبة الأداء والصيانة الوقائية والتصحيحية.")},
                ]},
            ],
        },

        # Projects with detailed cards (location / type / power / contract).
        "projects": {
            "eyebrow": _("مشاريعنا"),
            "heading": _("مشاريع نفّذتها أزوليس"),
            "subtitle": _("مجموعة مختارة من مشاريع الطاقة الشمسية المنفّذة في المغرب وفرنسا."),
            "detailed": True,
            "items": [
                {"name": _("رويال منصور المضيق"), "image": "images/companies/azolis/projects/royal-mansour.jpg", "details": [
                    {"icon": "pin", "label": _("الموقع"), "value": _("المغرب")},
                    {"icon": "sun", "label": _("النوع"), "value": _("مظلّة وقوف كهروضوئية")},
                    {"icon": "doc", "label": _("العقد"), "value": _("EPC للإنتاج الذاتي")}]},
                {"name": _("مشروع صناعي (سرّي)"), "image": "images/companies/azolis/projects/confidential.jpg", "details": [
                    {"icon": "pin", "label": _("الموقع"), "value": _("المغرب")},
                    {"icon": "sun", "label": _("النوع"), "value": _("PV على الأسطح")},
                    {"icon": "bolt", "label": _("القدرة المركبة"), "value": "6 MWp"},
                    {"icon": "doc", "label": _("العقد"), "value": "PSA"}]},
                {"name": _("مرجان المنارة"), "image": "images/companies/azolis/projects/marjane-menara.jpg", "details": [
                    {"icon": "pin", "label": _("الموقع"), "value": _("المغرب")},
                    {"icon": "sun", "label": _("النوع"), "value": _("PV على الأسطح")},
                    {"icon": "bolt", "label": _("القدرة المركبة"), "value": "665 kWp"},
                    {"icon": "doc", "label": _("العقد"), "value": _("EPC للإنتاج الذاتي")}]},
                {"name": _("توتال إنرجي"), "image": "images/companies/azolis/projects/totalenergies.jpg", "details": [
                    {"icon": "pin", "label": _("الموقع"), "value": _("المغرب")},
                    {"icon": "sun", "label": _("النوع"), "value": _("PV على الأسطح (مواقع متعددة)")},
                    {"icon": "bolt", "label": _("القدرة المركبة"), "value": "30 × 12 kWp"},
                    {"icon": "doc", "label": _("العقد"), "value": _("EPC للإنتاج الذاتي")}]},
                {"name": _("فيرتيكال جرين"), "image": "images/companies/azolis/projects/vertical-green.jpg", "details": [
                    {"icon": "pin", "label": _("الموقع"), "value": _("المغرب")},
                    {"icon": "sun", "label": _("النوع"), "value": _("الضخّ بالطاقة الشمسية")},
                    {"icon": "bolt", "label": _("القدرة المركبة"), "value": "287 kWp"},
                    {"icon": "doc", "label": _("العقد"), "value": _("EPC للإنتاج الذاتي")}]},
                {"name": _("لصفار غاز"), "image": "images/companies/azolis/projects/lasfar-gaz.jpg", "details": [
                    {"icon": "pin", "label": _("الموقع"), "value": _("المغرب")},
                    {"icon": "sun", "label": _("النوع"), "value": _("محطة شمسية أرضية")},
                    {"icon": "bolt", "label": _("القدرة المركبة"), "value": "50 kWp"},
                    {"icon": "doc", "label": _("العقد"), "value": _("EPC للإنتاج الذاتي")}]},
                {"name": _("سيتروين"), "image": "images/companies/azolis/projects/citroen.jpg", "details": [
                    {"icon": "pin", "label": _("الموقع"), "value": _("فرنسا")},
                    {"icon": "sun", "label": _("النوع"), "value": _("PV على الأسطح")},
                    {"icon": "bolt", "label": _("القدرة المركبة"), "value": "119 kWp"},
                    {"icon": "doc", "label": _("العقد"), "value": _("تعرفة تغذية 20 سنة")}]},
                {"name": "SPIE", "image": "images/companies/azolis/projects/spie.jpg", "details": [
                    {"icon": "pin", "label": _("الموقع"), "value": _("فرنسا")},
                    {"icon": "sun", "label": _("النوع"), "value": _("PV على الأسطح")},
                    {"icon": "bolt", "label": _("القدرة المركبة"), "value": "100 kWp"},
                    {"icon": "doc", "label": _("العقد"), "value": _("EPC للإنتاج الذاتي")}]},
                {"name": _("الأراضي الزراعية"), "image": "images/companies/azolis/projects/domaines-agricoles.jpg", "details": [
                    {"icon": "pin", "label": _("الموقع"), "value": _("المغرب")},
                    {"icon": "sun", "label": _("النوع"), "value": _("الضخّ بالطاقة الشمسية")},
                    {"icon": "bolt", "label": _("القدرة المركبة"), "value": "180 kWp"},
                    {"icon": "doc", "label": _("العقد"), "value": _("EPC للإنتاج الذاتي")}]},
            ],
        },

        "contact": {
            "phone": "+33 1 64 70 78 48",
            "email": "contact@azolis.com",
            "website": "azolis.com",
            "website_url": "https://www.azolis.com",
            "offices": [_("فونتينبلو، فرنسا"), _("الدار البيضاء، المغرب")],
        },
    },
}
