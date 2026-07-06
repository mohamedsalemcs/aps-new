# -*- coding: utf-8 -*-
"""Contact page content for the APS Group corporate website.

Contacts come from "APS Company Contacts.xlsx" (group row) and the confirmed
Jeddah head-office address (Gulf Center, Al Madina Road). The page renders a
contact form, the group's primary contacts, the three offices, and a working
Google Maps embed. Maps to a future CMS "Page" model cleanly.

User-facing strings are wrapped in ``_()`` (gettext); English in
``locale/en/LC_MESSAGES/django.po``. Phone/email/map queries are NOT translated.
"""

from django.utils.translation import gettext_lazy as _

CONTACT_PAGE = {
    "seo": {
        "title": _("تواصل معنا | مجموعة APS للتجهيزات والمشاريع"),
        "description": _(
            "تواصل مع مجموعة APS: أرسل استفسارك أو طلب عرض السعر عبر النموذج، "
            "أو تواصل مباشرةً عبر الهاتف والبريد الإلكتروني، وزُر مكاتبنا في جدة "
            "والرياض والخبر."
        ),
        "type": "website",
    },

    "breadcrumb": [
        {"label": _("الرئيسية"), "href": "/"},
        {"label": _("تواصل معنا")},
    ],
    "eyebrow": _("تواصل معنا"),
    "title": _("لنبدأ الحديث حول مشروعك"),
    "lead": _(
        "فريقنا جاهز للإجابة عن استفساراتك وتقديم الدعم وإعداد عروض الأسعار. "
        "املأ النموذج وسنعاود التواصل معك في أقرب وقت، أو تواصل معنا مباشرةً "
        "عبر القنوات أدناه."
    ),

    # Primary group contacts (from the Excel contacts sheet)
    "channels": [
        {"icon": "phone", "label": _("اتصل بنا"),
         "value": "+966 9200 14 515", "href": "tel:+96692001451", "ltr": True,
         "note": _("خطنا الموحّد لجميع فروع المملكة")},
        {"icon": "mail", "label": _("راسلنا"),
         "value": "info@aps.com.sa", "href": "mailto:info@aps.com.sa", "ltr": True,
         "note": _("نردّ على رسائلك خلال يوم عمل واحد")},
        {"icon": "pin", "label": _("المقر الرئيسي"),
         "value": _("جدة، المملكة العربية السعودية"), "href": "", "ltr": False,
         "note": _("مركز الخليج، طريق المدينة")},
    ],

    # Message-subject choices (multi-select checkboxes in the form)
    "subjects": [
        _("طلب عرض سعر"),
        _("استفسار عن المنتجات والحلول"),
        _("الدعم الفني وما بعد البيع"),
        _("التوريد والشراكات"),
        _("استفسار عام"),
    ],

    # Offices — HQ address is confirmed; regional pins are city-level.
    "offices_heading": _("مكاتبنا"),
    "offices_subtitle": _("نخدم المملكة بالكامل من ثلاثة مكاتب، المقر الرئيسي في جدة ومكتبان إقليميان في الرياض والخبر."),
    "offices": [
        {
            "name": _("جدة"),
            "tag": _("المقر الرئيسي"),
            "address": _("الطابق السابع، مكتب 303، مركز الخليج، طريق المدينة، ص.ب 110281، جدة 21477"),
            "phone": "+966 9200 14 515",
            "email": "info@aps.com.sa",
            "map_query": "Gulf Center, Al Madinah Road, Jeddah 21477",
            "is_hq": True,
        },
        {
            "name": _("الرياض"),
            "tag": _("مكتب إقليمي"),
            "address": _("الرياض، المملكة العربية السعودية"),
            "phone": "+966 9200 14 515",
            "email": "info@aps.com.sa",
            "map_query": "Riyadh, Saudi Arabia",
            "is_hq": False,
        },
        {
            "name": _("الخبر"),
            "tag": _("مكتب إقليمي"),
            "address": _("الخبر، المنطقة الشرقية، المملكة العربية السعودية"),
            "phone": "+966 9200 14 515",
            "email": "info@aps.com.sa",
            "map_query": "Al Khobar, Eastern Province, Saudi Arabia",
            "is_hq": False,
        },
    ],
}
