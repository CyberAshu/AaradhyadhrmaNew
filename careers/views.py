from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils import timezone
from .models import Job, JobApplication
from .forms import JobApplicationForm

def careers_list(request):
    active_jobs = Job.objects.filter(is_active=True)
    
    # Filter jobs with no closing date or closing date in the future
    open_jobs = [job for job in active_jobs if not job.closing_date or job.closing_date >= timezone.now().date()]
    
    context = {
        'page_title': 'Careers - Aaradhyadhrma',
        'meta_description': 'Explore exciting career opportunities at Aaradhyadhrma. Join our team of technology professionals and work on innovative projects.',
        'meta_keywords': 'careers, jobs, employment, technology jobs, software jobs, IT careers, Aaradhyadhrma careers',
        'og_title': 'Career Opportunities at Aaradhyadhrma',
        'og_description': 'Find your next career opportunity with Aaradhyadhrma. Join our innovative team of technology professionals.',
        'jobs': open_jobs,
    }
    return render(request, 'careers/careers_list.html', context)

def job_detail(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check if job is still open
    is_closed = job.closing_date and job.closing_date < timezone.now().date()
    
    context = {
        'page_title': f'{job.title} - Aaradhyadhrma Careers',
        'meta_description': f'Apply for the {job.title} position at Aaradhyadhrma. Learn about the role, requirements, and benefits.',
        'meta_keywords': f'{job.title}, job opening, career, employment, Aaradhyadhrma, {job.location}',
        'og_title': f'{job.title} - Job Opening at Aaradhyadhrma',
        'og_description': f'We are hiring for {job.title} at {job.location}. Apply now!',
        'job': job,
        'is_closed': is_closed,
    }
    return render(request, 'careers/job_detail.html', context)

def job_apply(request, job_id):
    job = get_object_or_404(Job, id=job_id, is_active=True)
    
    # Check if job is still open
    if job.closing_date and job.closing_date < timezone.now().date():
        messages.error(request, 'This position is no longer accepting applications.')
        return redirect('careers:job_detail', job_id=job.id)
    
    if request.method == 'POST':
        form = JobApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.application_date = timezone.now()
            application.save()
            messages.success(request, 'Your application has been submitted successfully!')
            return redirect('careers:job_detail', job_id=job.id)
    else:
        form = JobApplicationForm()
    
    context = {
        'page_title': f'Apply for {job.title} - Aaradhyadhrma Careers',
        'meta_description': f'Submit your application for the {job.title} position at Aaradhyadhrma. Join our team and grow your career.',
        'meta_keywords': f'job application, {job.title}, apply now, Aaradhyadhrma careers, job opportunity',
        'og_title': f'Apply for {job.title} - Aaradhyadhrma',
        'og_description': f'Submit your application for the {job.title} position. We look forward to reviewing your qualifications.',
        'job': job,
        'form': form,
    }
    return render(request, 'careers/job_apply.html', context)
