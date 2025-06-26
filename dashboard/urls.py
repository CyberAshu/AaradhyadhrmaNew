from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('blog/', views.blog_list, name='blog_list'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/edit/<int:pk>/', views.blog_edit, name='blog_edit'),
    path('blog/delete/<int:pk>/', views.blog_delete, name='blog_delete'),
    path('categories/', views.categories_list, name='categories_list'),
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('categories/delete/<int:pk>/', views.category_delete, name='category_delete'),
    path('team/', views.team_list, name='team_list'),
    path('team/create/', views.team_create, name='team_create'),
    path('team/edit/<int:pk>/', views.team_edit, name='team_edit'),
    path('team/delete/<int:pk>/', views.team_delete, name='team_delete'),
    path('careers/', views.careers_list, name='careers_list'),
    path('careers/create/', views.careers_create, name='careers_create'),
    path('careers/edit/<int:pk>/', views.careers_edit, name='careers_edit'),
    path('careers/delete/<int:pk>/', views.careers_delete, name='careers_delete'),
    path('users/', views.users_list, name='users_list'),
    path('users/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('contact-messages/', views.contact_messages_list, name='contact_messages_list'),
    path('contact-messages/delete/<int:pk>/', views.contact_message_delete, name='contact_message_delete'),
]
