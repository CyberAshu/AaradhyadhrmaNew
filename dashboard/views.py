from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from blog.models import Post, Category, Tag
from core.models import TeamMember, ContactMessage
from careers.models import Job, JobApplication
from django.db.models import Count, Q
from django.urls import reverse
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Helper function to check if user is staff
def is_staff(user):
    return user.is_staff

@login_required
@user_passes_test(is_staff)
def dashboard_home(request):
    """Dashboard home view with statistics and overview"""
    # Get statistics for the dashboard
    stats = {
        'total_posts': Post.objects.count(),
        'published_posts': Post.objects.filter(status='published').count(),
        'draft_posts': Post.objects.filter(status='draft').count(),
        'total_categories': Category.objects.count(),
        'total_tags': Tag.objects.count(),
        'total_team_members': TeamMember.objects.count(),
        'active_jobs': Job.objects.filter(is_active=True).count(),
        'total_job_applications': JobApplication.objects.count(),
        'total_contacts': ContactMessage.objects.count(),
        'users': User.objects.count(),
    }
    
    # Get recent activity
    recent_posts = Post.objects.order_by('-created_on')[:5]
    recent_applications = JobApplication.objects.order_by('-applied_date')[:5]
    recent_contacts = ContactMessage.objects.order_by('-date_sent')[:5]
    
    context = {
        'stats': stats,
        'recent_posts': recent_posts,
        'recent_applications': recent_applications,
        'recent_contacts': recent_contacts,
        'page_title': 'Dashboard - Aaradhyadhrma Admin',
    }
    return render(request, 'dashboard/index.html', context)

@login_required
@user_passes_test(is_staff)
def blog_list(request):
    """List view for blog posts with filtering and pagination"""
    posts = Post.objects.all().order_by('-created_on')
    
    # Filter by status if provided
    status = request.GET.get('status')
    if status and status in ['published', 'draft']:
        posts = posts.filter(status=status)
    
    # Filter by category if provided
    category_id = request.GET.get('category')
    if category_id:
        posts = posts.filter(category_id=category_id)
    
    # Search functionality
    search = request.GET.get('search')
    if search:
        posts = posts.filter(title__icontains=search)
    
    # Pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    categories = Category.objects.all()
    
    context = {
        'posts': posts,
        'categories': categories,
        'page_title': 'Blog Posts - Dashboard',
        'current_status': status,
        'current_category': category_id,
        'search_term': search,
    }
    return render(request, 'dashboard/blog/list.html', context)

@login_required
@user_passes_test(is_staff)
def blog_create(request):
    """View to create a new blog post"""
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    if request.method == 'POST':
        # Process form data
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        category_id = request.POST.get('category')
        content = request.POST.get('content')
        excerpt = request.POST.get('excerpt')
        status = request.POST.get('status', 'draft')
        featured_image = request.FILES.get('featured_image')
        selected_tags = request.POST.getlist('tags')
        
        # Create new post
        post = Post(
            title=title,
            slug=slug,
            category_id=category_id,
            content=content,
            excerpt=excerpt,
            status=status,
            author=request.user
        )
        
        if featured_image:
            post.featured_image = featured_image
            
        post.save()
        
        # Add tags
        post.tags.set(selected_tags)
        
        messages.success(request, 'Post created successfully!')
        return redirect('dashboard:blog_list')
    
    context = {
        'categories': categories,
        'tags': tags,
        'page_title': 'Create Post - Dashboard',
    }
    return render(request, 'dashboard/blog/create.html', context)

@login_required
@user_passes_test(is_staff)
def blog_edit(request, pk):
    """View to edit an existing blog post"""
    post = get_object_or_404(Post, pk=pk)
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    if request.method == 'POST':
        # Process form data
        post.title = request.POST.get('title')
        post.slug = request.POST.get('slug')
        post.category_id = request.POST.get('category')
        post.content = request.POST.get('content')
        post.excerpt = request.POST.get('excerpt')
        post.status = request.POST.get('status', 'draft')
        
        featured_image = request.FILES.get('featured_image')
        if featured_image:
            post.featured_image = featured_image
            
        selected_tags = request.POST.getlist('tags')
        post.tags.set(selected_tags)
        
        post.save()
        
        messages.success(request, 'Post updated successfully!')
        return redirect('dashboard:blog_list')
    
    context = {
        'post': post,
        'categories': categories,
        'tags': tags,
        'selected_tags': [tag.id for tag in post.tags.all()],
        'page_title': f'Edit Post: {post.title} - Dashboard',
    }
    return render(request, 'dashboard/blog/edit.html', context)

@login_required
@user_passes_test(is_staff)
def blog_delete(request, pk):
    """View to delete a blog post"""
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('dashboard:blog_list')
    
    context = {
        'post': post,
        'page_title': f'Delete Post: {post.title} - Dashboard',
    }
    return render(request, 'dashboard/blog/delete.html', context)

@login_required
@user_passes_test(is_staff)
def categories_list(request):
    """List view for blog categories"""
    categories = Category.objects.annotate(post_count=Count('posts'))
    
    context = {
        'categories': categories,
        'page_title': 'Categories - Dashboard',
    }
    return render(request, 'dashboard/blog/categories.html', context)

@login_required
@user_passes_test(is_staff)
def category_create(request):
    """View to create a new category"""
    if request.method == 'POST':
        name = request.POST.get('name')
        slug = request.POST.get('slug')
        description = request.POST.get('description')
        
        Category.objects.create(
            name=name,
            slug=slug,
            description=description
        )
        
        messages.success(request, 'Category created successfully!')
        return redirect('dashboard:categories_list')
    
    context = {
        'page_title': 'Create Category - Dashboard',
    }
    return render(request, 'dashboard/blog/category_form.html', context)

@login_required
@user_passes_test(is_staff)
def category_edit(request, pk):
    """View to edit an existing category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.slug = request.POST.get('slug')
        category.description = request.POST.get('description')
        category.save()
        
        messages.success(request, 'Category updated successfully!')
        return redirect('dashboard:categories_list')
    
    context = {
        'category': category,
        'page_title': f'Edit Category: {category.name} - Dashboard',
    }
    return render(request, 'dashboard/blog/category_form.html', context)

@login_required
@user_passes_test(is_staff)
def category_delete(request, pk):
    """View to delete a category"""
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        try:
            category.delete()
            messages.success(request, 'Category deleted successfully!')
        except Exception as e:
            messages.error(request, f'Cannot delete category: {str(e)}')
        return redirect('dashboard:categories_list')
    
    context = {
        'category': category,
        'page_title': f'Delete Category: {category.name} - Dashboard',
    }
    return render(request, 'dashboard/blog/category_delete.html', context)

@login_required
@user_passes_test(is_staff)
def team_list(request):
    """List view for team members"""
    team_members = TeamMember.objects.all()
    
    context = {
        'team_members': team_members,
        'page_title': 'Team Members - Dashboard',
    }
    return render(request, 'dashboard/team/list.html', context)

@login_required
@user_passes_test(is_staff)
def team_create(request):
    """View to create a new team member"""
    if request.method == 'POST':
        # Process form data
        name = request.POST.get('name')
        position = request.POST.get('position')
        bio = request.POST.get('bio')
        avatar = request.FILES.get('avatar')
        linkedin = request.POST.get('linkedin')
        github = request.POST.get('github')
        twitter = request.POST.get('twitter')
        order = request.POST.get('order', 0)
        is_active = request.POST.get('is_active') == 'on'
        
        # Create team member
        team_member = TeamMember(
            name=name,
            position=position,
            bio=bio,
            linkedin=linkedin,
            github=github,
            twitter=twitter,
            order=order,
            is_active=is_active
        )
        
        if avatar:
            team_member.avatar = avatar
            
        team_member.save()
        
        messages.success(request, 'Team member added successfully!')
        return redirect('dashboard:team_list')
    
    context = {
        'page_title': 'Add Team Member - Dashboard',
    }
    return render(request, 'dashboard/team/create.html', context)

@login_required
@user_passes_test(is_staff)
def team_edit(request, pk):
    """View to edit an existing team member"""
    team_member = get_object_or_404(TeamMember, pk=pk)
    
    if request.method == 'POST':
        # Process form data
        team_member.name = request.POST.get('name')
        team_member.position = request.POST.get('position')
        team_member.bio = request.POST.get('bio')
        team_member.linkedin = request.POST.get('linkedin')
        team_member.github = request.POST.get('github')
        team_member.twitter = request.POST.get('twitter')
        team_member.order = request.POST.get('order', 0)
        team_member.is_active = request.POST.get('is_active') == 'on'
        
        avatar = request.FILES.get('avatar')
        if avatar:
            team_member.avatar = avatar
            
        team_member.save()
        
        messages.success(request, 'Team member updated successfully!')
        return redirect('dashboard:team_list')
    
    context = {
        'team_member': team_member,
        'page_title': f'Edit Team Member: {team_member.name} - Dashboard',
    }
    return render(request, 'dashboard/team/edit.html', context)

@login_required
@user_passes_test(is_staff)
def team_delete(request, pk):
    """View to delete a team member"""
    team_member = get_object_or_404(TeamMember, pk=pk)
    
    if request.method == 'POST':
        team_member.delete()
        messages.success(request, 'Team member deleted successfully!')
        return redirect('dashboard:team_list')
    
    context = {
        'team_member': team_member,
        'page_title': f'Delete Team Member: {team_member.name} - Dashboard',
    }
    return render(request, 'dashboard/team/delete.html', context)

@login_required
@user_passes_test(is_staff)
def careers_list(request):
    """List view for job listings"""
    jobs = Job.objects.all()
    applications = JobApplication.objects.all().order_by('-applied_date')
    
    context = {
        'jobs': jobs,
        'applications': applications,
        'page_title': 'Job Listings - Dashboard',
    }
    return render(request, 'dashboard/careers/list.html', context)

@login_required
@user_passes_test(is_staff)
def careers_create(request):
    """View to create a new job listing"""
    if request.method == 'POST':
        # Process form data
        title = request.POST.get('title')
        slug = request.POST.get('slug')
        location = request.POST.get('location')
        employment_type = request.POST.get('employment_type')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')
        responsibilities = request.POST.get('responsibilities')
        benefits = request.POST.get('benefits')
        is_active = request.POST.get('is_active') == 'on'
        
        # Create job
        job = Job(
            title=title,
            slug=slug,
            location=location,
            employment_type=employment_type,
            description=description,
            requirements=requirements,
            responsibilities=responsibilities,
            benefits=benefits,
            is_active=is_active
        )
        
        job.save()
        
        messages.success(request, 'Job listing created successfully!')
        return redirect('dashboard:careers_list')
    
    context = {
        'page_title': 'Create Job Listing - Dashboard',
    }
    return render(request, 'dashboard/careers/create.html', context)

@login_required
@user_passes_test(is_staff)
def careers_edit(request, pk):
    """View to edit an existing job listing"""
    job = get_object_or_404(Job, pk=pk)
    
    if request.method == 'POST':
        # Process form data
        job.title = request.POST.get('title')
        job.slug = request.POST.get('slug')
        job.location = request.POST.get('location')
        job.employment_type = request.POST.get('employment_type')
        job.description = request.POST.get('description')
        job.requirements = request.POST.get('requirements')
        job.responsibilities = request.POST.get('responsibilities')
        job.benefits = request.POST.get('benefits')
        job.is_active = request.POST.get('is_active') == 'on'
        
        job.save()
        
        messages.success(request, 'Job listing updated successfully!')
        return redirect('dashboard:careers_list')
    
    context = {
        'job': job,
        'page_title': f'Edit Job: {job.title} - Dashboard',
    }
    return render(request, 'dashboard/careers/edit.html', context)

@login_required
@user_passes_test(is_staff)
def careers_delete(request, pk):
    """View to delete a job listing"""
    job = get_object_or_404(Job, pk=pk)
    
    if request.method == 'POST':
        job.delete()
        messages.success(request, 'Job listing deleted successfully!')
        return redirect('dashboard:careers_list')
    
    context = {
        'job': job,
        'page_title': f'Delete Job: {job.title} - Dashboard',
    }
    return render(request, 'dashboard/careers/delete.html', context)

@login_required
@user_passes_test(is_staff)
def users_list(request):
    """List view for users"""
    users = User.objects.all()
    
    context = {
        'users': users,
        'page_title': 'Users - Dashboard',
    }
    return render(request, 'dashboard/users/list.html', context)

@login_required
@user_passes_test(is_staff)
def user_edit(request, pk):
    """View to edit a user"""
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        # Process form data
        user.first_name = request.POST.get('first_name', '')
        user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.is_active = 'is_active' in request.POST
        user.is_staff = 'is_staff' in request.POST
        user.is_superuser = 'is_superuser' in request.POST
        
        # Update password if provided
        password = request.POST.get('password')
        if password:
            user.set_password(password)
        
        user.save()
        messages.success(request, f'User {user.username} has been updated.')
        return redirect('dashboard:users_list')
    
    context = {
        'user_edit': user,
        'page_title': f'Edit User: {user.username} - Aaradhyadhrma Admin'
    }
    return render(request, 'dashboard/user_edit.html', context)


@login_required
@user_passes_test(is_staff)
def contact_messages_list(request):
    """View to list all contact messages with search and pagination"""
    contact_messages = ContactMessage.objects.all().order_by('-date_sent')
    
    # Search functionality
    search_query = request.GET.get('q', '')
    if search_query:
        contact_messages = contact_messages.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(message__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(contact_messages, 20)  # Show 20 messages per page
    page = request.GET.get('page')
    
    try:
        messages_page = paginator.page(page)
    except PageNotAnInteger:
        messages_page = paginator.page(1)
    except EmptyPage:
        messages_page = paginator.page(paginator.num_pages)
    
    context = {
        'contact_messages': messages_page,
        'search_query': search_query,
        'total_messages': contact_messages.count(),
        'page_title': 'Contact Messages - Aaradhyadhrma Admin'
    }
    return render(request, 'dashboard/contact/contact_messages_list.html', context)


@login_required
@user_passes_test(is_staff)
def contact_message_delete(request, pk):
    """View to delete a contact message"""
    message = get_object_or_404(ContactMessage, pk=pk)
    if request.method == 'POST':
        message.delete()
        messages.success(request, 'Contact message has been deleted successfully.')
        return redirect('dashboard:contact_messages_list')
    
    # If not a POST request, show confirmation page
    context = {
        'message': message,
        'page_title': 'Delete Contact Message - Aaradhyadhrma Admin'
    }
    return render(request, 'dashboard/contact/contact_message_confirm_delete.html', context)
