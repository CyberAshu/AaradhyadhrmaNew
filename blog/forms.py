from django import forms
from .models import Comment, Newsletter

class CommentForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your Email'
    }))
    body = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Your Comment',
        'rows': 4
    }))
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']


class NewsletterForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'newsletter-input',
        'placeholder': 'Your Email Address'
    }))
    
    class Meta:
        model = Newsletter
        fields = ['email']
