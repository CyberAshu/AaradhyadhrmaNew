from django import forms
from .models import JobApplication

class JobApplicationForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Full Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Email'
    }))
    phone = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Phone Number'
    }))
    resume = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'form-control',
    }), help_text='Upload your resume (PDF or DOC format)')
    cover_letter = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Your Cover Letter (Optional)',
        'rows': 5
    }))
    linkedin = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'LinkedIn Profile URL (Optional)'
    }))
    github = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'GitHub Profile URL (Optional)'
    }))
    portfolio = forms.URLField(required=False, widget=forms.URLInput(attrs={
        'class': 'form-control',
        'placeholder': 'Portfolio Website URL (Optional)'
    }))
    
    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'resume', 'cover_letter', 'linkedin', 'github', 'portfolio']
