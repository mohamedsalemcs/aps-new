# -*- coding: utf-8 -*-
"""Populate the English (``*_en``) columns of the CMS from the gettext catalog.

The CMS was seeded with Arabic content only, so ``pick()`` falls back to Arabic
on the English site. Every editorial Arabic string also lives (translated) in
``locale/en/LC_MESSAGES/django.po``; this command walks all ``website`` models,
and for each empty ``<base>_en`` field looks up the English translation of the
matching ``<base>_ar`` value via ``gettext`` and stores it.

Multi-line fields (bullets, offices) are translated line by line. Anything not
found in the catalog is left blank (Arabic fallback stays) and reported.

Idempotent: only fills EMPTY ``_en`` fields, so re-running is safe. Pass
``--overwrite`` to also refresh non-empty ones.

    python manage.py fill_en_from_po
"""
from django.apps import apps
from django.core.management.base import BaseCommand
from django.utils import translation


class Command(BaseCommand):
    help = "Fill empty *_en CMS fields from the gettext (en) catalog."

    def add_arguments(self, parser):
        parser.add_argument("--overwrite", action="store_true",
                            help="Also replace *_en fields that already have a value.")

    def handle(self, *args, **opts):
        overwrite = opts["overwrite"]
        translation.activate("en")
        gettext = translation.gettext

        def tr(value):
            """Translate a possibly multi-line Arabic value; keep untranslated lines."""
            if not value:
                return value, True
            parts = value.split("\n")
            out, all_found = [], True
            for p in parts:
                s = p.strip()
                if not s:
                    out.append(p)
                    continue
                en = gettext(s)
                if en == s:            # not in catalog
                    all_found = False
                out.append(en)
            return "\n".join(out), all_found

        filled = 0
        missing = set()
        for model in apps.get_app_config("website").get_models():
            names = {f.name for f in model._meta.fields}
            pairs = [(n[:-3], n, n[:-3] + "_en") for n in names
                     if n.endswith("_ar") and (n[:-3] + "_en") in names]
            if not pairs:
                continue
            for obj in model.objects.all():
                changed = False
                for _base, ar_f, en_f in pairs:
                    ar_v = (getattr(obj, ar_f) or "").strip("\n")
                    en_v = getattr(obj, en_f) or ""
                    if not ar_v or (en_v and not overwrite):
                        continue
                    new_v, found = tr(ar_v)
                    if new_v and new_v != ar_v:
                        setattr(obj, en_f, new_v)
                        changed = True
                    if not found:
                        for ln in ar_v.split("\n"):
                            ln = ln.strip()
                            if ln and gettext(ln) == ln:
                                missing.add(ln)
                if changed:
                    obj.save()
                    filled += 1

        translation.deactivate()
        self.stdout.write(self.style.SUCCESS(f"Updated {filled} row(s)."))
        if missing:
            self.stdout.write(self.style.WARNING(
                f"{len(missing)} Arabic string(s) had no English in the catalog:"))
            for m in sorted(missing):
                self.stdout.write("  - " + m)
