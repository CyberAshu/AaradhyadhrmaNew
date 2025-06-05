from django.db import models
from django.urls import reverse

class Job(models.Model):
    EMPLOYMENT_TYPE_CHOICES = (
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    )
    
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    location = models.CharField(max_length=100)
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES)
    description = models.TextField()
    responsibilities = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    posted_date = models.DateField(auto_now_add=True)
    closing_date = models.DateField(blank=True, null=True)
    
    class Meta:
        ordering = ['-posted_date']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('careers:job_detail', kwargs={'job_id': self.id})

class JobApplication(models.Model):
    STATUS_CHOICES = (
        ('received', 'Received'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview'),
        ('selected', 'Selected'),
        ('rejected', 'Rejected'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField(blank=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    portfolio = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='received')
    notes = models.TextField(blank=True)
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-applied_date']
    
    def __str__(self):
        return f"{self.name} - {self.job.title}"
