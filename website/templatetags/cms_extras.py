# -*- coding: utf-8 -*-
"""Small template helpers for the custom CMS admin templates."""
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# Outline (stroke) icons — Feather/Lucide style (MIT), inlined for a
# consistent, self-contained icon set across the admin.
_ICONS = {
    "grid": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/>',
    "home": '<path d="M3 9.5L12 3l9 6.5"/><path d="M5 10v10a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V10"/><path d="M9 21v-6h6v6"/>',
    "info": '<circle cx="12" cy="12" r="10"/><line x1="12" y1="16" x2="12" y2="11"/><line x1="12" y1="8" x2="12.01" y2="8"/>',
    "help": '<circle cx="12" cy="12" r="10"/><path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "mail": '<rect x="2" y="4" width="20" height="16" rx="2"/><path d="M22 6l-10 7L2 6"/>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.362 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"/>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75"/>',
    "briefcase": '<rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/>',
    "inbox": '<path d="M22 12h-6l-2 3h-4l-2-3H2"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/>',
    "id": '<rect x="2" y="4" width="20" height="16" rx="2"/><circle cx="9" cy="10" r="2.2"/><path d="M5.5 16.5c.5-1.6 1.9-2.3 3.5-2.3s3 .7 3.5 2.3M15 9h4M15 12.5h4"/>',
    "settings": '<circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"/>',
    "menu": '<line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/>',
    "user": '<path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "logout": '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/>',
    "external": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15 3 21 3 21 9"/><line x1="10" y1="14" x2="21" y2="3"/>',
    "eye": '<path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
    "trash": '<polyline points="3 6 5 6 21 6"/><path d="M19 6v14a2 2 0 0 1-2 2H7a2 2 0 0 1-2-2V6m3 0V4a2 2 0 0 1 2-2h4a2 2 0 0 1 2 2v2"/><line x1="10" y1="11" x2="10" y2="17"/><line x1="14" y1="11" x2="14" y2="17"/>',
    "save": '<path d="M19 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11l5 5v11a2 2 0 0 1-2 2z"/><polyline points="17 21 17 13 7 13 7 21"/><polyline points="7 3 7 8 15 8"/>',
    "discard": '<polyline points="1 4 1 10 7 10"/><path d="M3.51 15a9 9 0 1 0 2.13-9.36L1 10"/>',
    "alert": '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12" y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>',
    "plus": '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>',
    "image": '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.6"/><path d="M21 15l-5-5L5 21"/>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"/>',
    "up": '<line x1="12" y1="19" x2="12" y2="5"/><polyline points="5 12 12 5 19 12"/>',
    "down": '<line x1="12" y1="5" x2="12" y2="19"/><polyline points="19 12 12 19 5 12"/>',
    "chevron": '<polyline points="6 9 12 15 18 9"/>',
    "chevron-up": '<polyline points="18 15 12 9 6 15"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><polyline points="12 7 12 12 15 14"/>',
    "chevrons-right": '<polyline points="13 17 18 12 13 7"/><polyline points="6 17 11 12 6 7"/>',
    "chevrons-left": '<polyline points="11 17 6 12 11 7"/><polyline points="18 17 13 12 18 7"/>',
}


@register.simple_tag
def icon(name, size=18, cls=""):
    body = _ICONS.get(name, "")
    return mark_safe(
        '<svg class="fi %s" width="%s" height="%s" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" stroke-linecap="round" '
        'stroke-linejoin="round" aria-hidden="true">%s</svg>' % (cls, size, size, body)
    )


@register.filter
def widget_type(field):
    """Lowercased widget class name, e.g. 'clearablefileinput', 'checkboxinput'."""
    try:
        return field.field.widget.__class__.__name__.lower()
    except AttributeError:
        return ""


@register.filter
def is_file(field):
    return widget_type(field) in ("clearablefileinput", "fileinput")


@register.filter
def is_checkbox(field):
    return widget_type(field) == "checkboxinput"


@register.filter
def file_url(field):
    """Current URL of a bound file field, or '' when empty."""
    val = getattr(field, "value", lambda: None)()
    if not val:  # empty FieldFile is falsy (no name)
        return ""
    if isinstance(val, str):  # already a path/URL
        return val
    try:
        return val.url or ""
    except ValueError:  # FieldFile with no file associated
        return ""


@register.filter
def split_subjects(value):
    """Split a stored contact-message subjects string ("، "-joined) into a
    clean list for rendering as chips. Empty → []."""
    if not value:
        return []
    parts = str(value).replace("،", ",").split(",")
    return [p.strip() for p in parts if p.strip()]
