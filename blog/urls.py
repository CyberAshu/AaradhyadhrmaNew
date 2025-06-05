from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='blog_list'),
    path('search/', views.blog_search, name='blog_search'),
    path('tag/<slug:tag_slug>/', views.blog_tag, name='blog_tag'),
    path('category/<slug:category_slug>/', views.blog_category, name='blog_category'),
    path('newsletter/subscribe/', views.newsletter_subscribe, name='newsletter_subscribe'),
    path('newsletter/confirm/<uuid:token>/', views.newsletter_confirm, name='newsletter_confirm'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
]
