# -*- coding: utf-8 -*-
"""URL routes for the custom CMS admin, mounted at ``/manage/``."""
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from . import cms_views as v

app_name = "cms"

urlpatterns = [
    path("login/", v.login_view, name="login"),
    path("logout/", v.logout_view, name="logout"),
    path("profile/", v.profile, name="profile"),
    # Password reset via email (dev: console backend prints the link).
    path("password-reset/", auth_views.PasswordResetView.as_view(
        template_name="manage/pw_reset.html",
        email_template_name="manage/pw_reset_email.html",
        subject_template_name="manage/pw_reset_subject.txt",
        success_url=reverse_lazy("cms:pw_reset_done")), name="pw_reset"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view(
        template_name="manage/pw_reset_done.html"), name="pw_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(
        template_name="manage/pw_reset_confirm.html",
        success_url=reverse_lazy("cms:pw_reset_complete")), name="pw_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(
        template_name="manage/pw_reset_complete.html"), name="pw_reset_complete"),
    path("", v.dashboard, name="dashboard"),
    path("home/", v.home_edit, name="home"),
    path("inbox/", v.inbox, name="inbox"),
    path("inbox/<int:pk>/", v.inbox_detail, name="inbox_detail"),
    path("settings/", v.settings_edit, name="settings"),
    path("group/", v.group_edit, name="group"),
    path("site/", v.site_edit, name="site"),
    path("about/", v.about_edit, name="about"),
    path("about/facts/", v.about_facts, name="about_facts"),
    path("about/items/<slug:group>/", v.about_items, name="about_items"),
    path("faq/", v.faq_edit, name="faq"),
    path("faq/stats/", v.faq_stats, name="faq_stats"),
    path("faq/categories/", v.faq_categories, name="faq_categories"),
    path("faq/categories/<int:pk>/items/", v.faq_items, name="faq_items"),
    path("contact/", v.contact_edit, name="contact"),
    path("contact/channels/", v.contact_channels, name="contact_channels"),
    path("contact/offices/", v.contact_offices, name="contact_offices"),
    path("partners-page/", v.partners_page_edit, name="partners_page"),
    path("partners-page/facts/", v.partners_facts, name="partners_facts"),
    path("companies/", v.company_list, name="companies"),
    path("companies/add/", v.company_add, name="company_add"),
    path("companies/<slug:slug>/", v.company_edit, name="company_edit"),
    path("companies/<slug:slug>/delete/", v.company_delete, name="company_delete"),
    path("companies/<slug:slug>/toggle/", v.company_toggle_publish, name="company_toggle_publish"),
    # Section editors
    path("companies/<slug:slug>/facts/", v.facts_edit, name="facts_edit"),
    path("companies/<slug:slug>/systems/", v.systems_edit, name="systems_edit"),
    path("companies/<slug:slug>/projects/", v.projects_edit, name="projects_edit"),
    path("companies/<slug:slug>/projects/<int:pk>/details/", v.project_details_edit, name="project_details_edit"),
    path("companies/<slug:slug>/partners/", v.partners_edit, name="partners_edit"),
    path("companies/<slug:slug>/guiding/", v.guiding_edit, name="guiding_edit"),
    path("companies/<slug:slug>/lifecycle/", v.lifecycle_edit, name="lifecycle_edit"),
    path("companies/<slug:slug>/lifecycle/<int:pk>/steps/", v.phase_steps_edit, name="phase_steps_edit"),
]
