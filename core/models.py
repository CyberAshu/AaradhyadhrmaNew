from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

class Skill(models.Model):
    name = models.CharField(max_length=50)
    level = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(100)])
    team_member = models.ForeignKey('TeamMember', on_delete=models.CASCADE, related_name='skills')
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f"{self.name} - {self.level}%"

class Project(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    tech_stack = models.CharField(max_length=255, help_text="Comma-separated list of technologies used")
    team_member = models.ForeignKey('TeamMember', on_delete=models.CASCADE, related_name='projects')
    order = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title
    
    def tech_stack_list(self):
        return [tech.strip() for tech in self.tech_stack.split(',')]

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    department = models.CharField(max_length=50, default='development')
    experience = models.PositiveIntegerField(default=1, help_text="Years of experience")
    
    def save(self, *args, **kwargs):
        # If this is an existing object and we're updating the photo
        if self.pk:
            try:
                # Get the old instance to check if photo has changed
                old_instance = TeamMember.objects.get(pk=self.pk)
                if old_instance.photo and self.photo and old_instance.photo != self.photo:
                    # Delete the old photo file
                    old_instance.photo.delete(save=False)
            except TeamMember.DoesNotExist:
                pass
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    company = models.CharField(max_length=100, blank=True)
    comment = models.TextField()
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    photo = models.ImageField(upload_to='testimonials/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_added']
    
    def __str__(self):
        return f"{self.name} - {self.rating} stars"

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    inquiry_type = models.CharField(max_length=50, blank=True, null=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-date_sent']
    
    def __str__(self):
        return f"{self.name} - {self.subject}"

class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    message = models.TextField()
    date_submitted = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    source = models.CharField(max_length=50, default='website', help_text="Source of the contact form (website, chatbot, etc.)")
    
    class Meta:
        ordering = ['-date_submitted']
    
    def __str__(self):
        return f"Contact from {self.name} - {self.date_submitted.strftime('%Y-%m-%d %H:%M')}"
