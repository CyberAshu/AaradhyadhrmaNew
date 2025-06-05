from django.contrib import admin
from .models import Job, JobApplication

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'employment_type', 'is_active', 'posted_date', 'closing_date')
    list_filter = ('is_active', 'employment_type', 'posted_date')
    search_fields = ('title', 'location', 'description', 'requirements')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_active',)
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'location', 'employment_type', 'salary_range')
        }),
        ('Description', {
            'fields': ('description', 'responsibilities', 'requirements')
        }),
        ('Status', {
            'fields': ('is_active', 'closing_date')
        }),
    )

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'job', 'applied_date', 'status')
    list_filter = ('status', 'applied_date', 'job')
    search_fields = ('name', 'email', 'phone', 'cover_letter', 'notes')
    readonly_fields = ('applied_date',)
    
    fieldsets = (
        ('Applicant Information', {
            'fields': ('job', 'name', 'email', 'phone')
        }),
        ('Application Details', {
            'fields': ('resume', 'cover_letter')
        }),
        ('Online Profiles', {
            'fields': ('linkedin', 'github', 'portfolio'),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('status', 'notes')
        }),
    )
