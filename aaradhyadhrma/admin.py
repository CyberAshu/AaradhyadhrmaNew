"""
Admin customization for Aaradhyadhrma Django project
This file contains global admin customizations that apply to all apps
"""

from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# Custom admin site configuration
admin.site.site_header = 'Aaradhyadhrma Admin'
admin.site.site_title = 'Aaradhyadhrma'
admin.site.index_title = 'Dashboard'
admin.site.enable_nav_sidebar = True


# Common admin mixins
class TimeStampedAdminMixin:
    """
    Mixin to display timestamp fields in admin list and make them readonly
    """
    readonly_fields = ('created_at', 'updated_at')
    list_filter = ('created_at', 'updated_at')


class SeoAdminMixin:
    """
    Mixin for SEO fields in admin
    """
    seo_fieldset = (
        _('SEO Options'), {
            'classes': ('collapse',),
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
        }
    )


class PublishableAdminMixin:
    """
    Mixin for models that can be published/unpublished
    """
    list_filter = ('is_active', 'created_at')
    list_display = ('__str__', 'is_active', 'created_at')
    actions = ['make_active', 'make_inactive']

    def make_active(self, request, queryset):
        queryset.update(is_active=True)
    make_active.short_description = _("Mark selected items as active")

    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
    make_inactive.short_description = _("Mark selected items as inactive")


class OrderableAdminMixin:
    """
    Mixin for models that can be ordered
    """
    list_display = ('__str__', 'order')
    list_editable = ('order',)
    ordering = ('order',)
