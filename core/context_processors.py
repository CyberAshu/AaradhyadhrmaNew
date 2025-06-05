"""
Context processors for the Aaradhyadhrma website
These will inject data into all templates
"""
from django.conf import settings
from core.models import TeamMember
from blog.models import Post, Category
from careers.models import Job
from datetime import datetime


def global_context(request):
    """
    Add commonly used data to the global template context
    """
    # Basic site info
    site_info = {
        'name': 'Aaradhyadhrma',
        'tagline': 'Ancient Wisdom, Modern Solution',
        'contact_email': 'info@aaradhyadhrma.com',
        'contact_phone': '+91 98765 43210',
        'address': '123 Tech Park, Bengaluru, Karnataka, India',
        'social_links': {
            'facebook': 'https://facebook.com/aaradhyadhrma',
            'twitter': 'https://twitter.com/aaradhyadhrma',
            'linkedin': 'https://linkedin.com/company/aaradhyadhrma',
            'github': 'https://github.com/aaradhyadhrma',
        },
        'copyright_year': datetime.now().year,
    }
    
    # Get active team members for footer/about sections
    team_members = TeamMember.objects.filter(is_active=True)[:5]
    
    # Get recent blog posts for sidebar/footer
    recent_posts = Post.objects.filter(status='published').order_by('-created_on')[:5]
    
    # Get all categories for blog navigation
    blog_categories = Category.objects.all()
    
    # Add default SEO and OpenGraph values for all pages
    og_image = request.build_absolute_uri('/static/images/logo.png')
    
    # Get job count for header/footer
    job_count = Job.objects.filter(is_active=True).count()
    
    return {
        'site_info': site_info,
        'team_members': team_members,
        'recent_posts': recent_posts,
        'blog_categories': blog_categories,
        'job_count': job_count,
        'og_image': og_image,
        'DEBUG': settings.DEBUG,
    }


def theme_context(request):
    """
    Handle theme preference (dark/light mode)
    """
    # Check if theme preference is stored in session
    # Default to light mode if not found
    theme_preference = request.session.get('theme_preference', 'light')
    
    return {
        'theme_preference': theme_preference,
    }
