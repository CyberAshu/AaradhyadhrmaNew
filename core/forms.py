from django import forms
from .models import ContactMessage

class ContactForm(forms.ModelForm):
    INQUIRY_CHOICES = [
        ('general', 'General Inquiry'),
        ('services', 'Services Information'),
        ('quote', 'Request a Quote'),
        ('support', 'Technical Support'),
        ('career', 'Career Inquiry'),
    ]
    
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Email'
    }))
    subject = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Subject'
    }))
    inquiry_type = forms.ChoiceField(choices=INQUIRY_CHOICES, widget=forms.Select(attrs={
        'class': 'form-select',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Your Message',
        'rows': 5
    }))
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'inquiry_type', 'message']
