from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('team/', views.team, name='team'),
    path('team/<int:member_id>/', views.team_member_detail, name='team_member_detail'),
    path('testimonials/', views.testimonials, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('offline/', views.offline, name='offline'),
    path('case-study/<slug:slug>/', views.case_study, name='case_study'),
    path('privacy-policy/', TemplateView.as_view(template_name='core/privacy-policy.html'), name='privacy_policy'),
    path('terms-of-service/', TemplateView.as_view(template_name='core/terms-of-service.html'), name='terms_of_service'),
]
