from django.urls import path

from . import views

app_name = 'website'

urlpatterns = [
    path('', views.home, name='home'),
    path('home-slider/', views.home_slider, name='home_slider'),
    path('about/', views.about, name='about'),
    path('partners/', views.partners, name='partners'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('companies/<slug:slug>/', views.company, name='company'),
]
