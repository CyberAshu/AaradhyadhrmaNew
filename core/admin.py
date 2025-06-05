from django.contrib import admin
from .models import TeamMember, Testimonial, ContactMessage, Skill, Project, ContactForm

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'position', 'bio')
    list_editable = ('order', 'is_active')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'date_added', 'is_active')
    list_filter = ('rating', 'is_active')
    search_fields = ('name', 'company', 'comment')
    list_editable = ('is_active',)

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'inquiry_type', 'date_sent', 'is_read')
    list_filter = ('inquiry_type', 'is_read', 'date_sent')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('date_sent',)
    
    def has_add_permission(self, request):
        return False  # Prevent adding new messages from admin

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'team_member', 'order')
    list_filter = ('team_member',)
    search_fields = ('name', 'team_member__name')
    list_editable = ('level', 'order')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'team_member', 'order')
    list_filter = ('team_member',)
    search_fields = ('title', 'description', 'team_member__name')
    list_editable = ('order',)

@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date_submitted', 'is_processed', 'source')
    list_filter = ('is_processed', 'date_submitted', 'source')
    search_fields = ('name', 'email', 'phone', 'message')
    list_editable = ('is_processed',)
    readonly_fields = ('date_submitted',)
    
    def has_add_permission(self, request):
        return False  # Prevent adding new submissions from admin
        
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.source == 'chatbot':
            form.base_fields['message'].help_text = "This message was submitted through the chatbot interface."
        return form
