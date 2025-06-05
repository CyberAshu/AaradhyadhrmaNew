from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
from .models import Post, Category, Tag, Comment, Newsletter
from .forms import CommentForm, NewsletterForm

def blog_list(request):
    posts = Post.objects.filter(status='published').order_by('-published_on')
    recent_posts = Post.objects.filter(status='published').order_by('-published_on')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'page_title': 'Blog - Aaradhyadhrma',
        'meta_description': 'Explore our tech insights, industry news, and software development articles. Stay updated with the latest in technology trends and innovations.',
        'meta_keywords': 'blog, tech blog, software development, AI, machine learning, technology news',
        'og_title': 'Blog - Aaradhyadhrma',
        'og_description': 'Discover articles on software development, AI, and technology trends from our expert team.',
        'posts': posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    recent_posts = Post.objects.filter(status='published').order_by('-published_on')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # Related posts - posts with same category or tags
    related_posts = Post.objects.filter(category=post.category, status='published').exclude(id=post.id)[:3]
    
    # Comment form and submission handling
    new_comment = None
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('blog:blog_detail', slug=post.slug)
    else:
        form = CommentForm()
    
    # Prepare meta description from post excerpt or truncated content
    meta_description = post.excerpt if post.excerpt else post.content[:150] + '...'
    
    context = {
        'page_title': f'{post.title} - Aaradhyadhrma Blog',
        'meta_description': meta_description,
        'meta_keywords': f'{post.category}, {", ".join([tag.name for tag in post.tags.all()])}, blog post, Aaradhyadhrma',
        'og_title': post.title,
        'og_description': meta_description,
        'post': post,
        'comments': comments,
        'form': form,
        'new_comment': new_comment,
        'related_posts': related_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/blog_detail.html', context)

def blog_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(category=category, status='published').order_by('-published_on')
    recent_posts = Post.objects.filter(status='published').order_by('-published_on')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'page_title': f'{category.name} - Aaradhyadhrma Blog',
        'meta_description': f'Browse articles about {category.name}. Find insights and updates on {category.name} from Aaradhyadhrma experts.',
        'meta_keywords': f'{category.name}, blog, technology, Aaradhyadhrma, articles',
        'og_title': f'{category.name} - Aaradhyadhrma Blog',
        'og_description': f'Articles categorized under {category.name} - Technology insights from Aaradhyadhrma',
        'category': category,
        'posts': posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/blog_category.html', context)

def blog_tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = Post.objects.filter(tags__in=[tag], status='published').order_by('-published_on')
    recent_posts = Post.objects.filter(status='published').order_by('-published_on')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'page_title': f'{tag.name} - Aaradhyadhrma Blog',
        'meta_description': f'Browse articles tagged with {tag.name}. Find insights and updates on {tag.name} from Aaradhyadhrma experts.',
        'meta_keywords': f'{tag.name}, blog, technology, Aaradhyadhrma, articles',
        'og_title': f'{tag.name} - Aaradhyadhrma Blog',
        'og_description': f'Articles tagged with {tag.name} - Technology insights from Aaradhyadhrma',
        'tag': tag,
        'posts': posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/blog_tag.html', context)

def blog_search(request):
    query = request.GET.get('q', '')
    recent_posts = Post.objects.filter(status='published').order_by('-published_on')[:3]
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    if query:
        # Search in title, content, and excerpt
        posts = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(excerpt__icontains=query),
            status='published'
        ).order_by('-published_on')
    else:
        posts = Post.objects.filter(status='published').order_by('-published_on')
    
    # Pagination
    paginator = Paginator(posts, 6)  # Show 6 posts per page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results
        posts = paginator.page(paginator.num_pages)
    
    context = {
        'page_title': f'Search Results for "{query}" - Aaradhyadhrma Blog',
        'meta_description': f'Search results for {query} in Aaradhyadhrma blog posts.',
        'meta_keywords': f'search, {query}, blog, Aaradhyadhrma',
        'posts': posts,
        'query': query,
        'recent_posts': recent_posts,
        'categories': categories,
        'tags': tags,
    }
    return render(request, 'blog/blog_search.html', context)


def newsletter_subscribe(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            # Check if email already exists
            existing_subscriber = Newsletter.objects.filter(email=email).first()
            
            if existing_subscriber:
                if existing_subscriber.confirmed:
                    return JsonResponse({
                        'status': 'info',
                        'message': 'You are already subscribed to our newsletter.'
                    })
                else:
                    # Resend confirmation email
                    send_confirmation_email(existing_subscriber)
                    return JsonResponse({
                        'status': 'success',
                        'message': 'A confirmation email has been sent to your email address.'
                    })
            
            # Create new subscriber
            subscriber = form.save()
            
            # Send confirmation email
            send_confirmation_email(subscriber)
            
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for subscribing! Please check your email to confirm your subscription.'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'Please enter a valid email address.'
            })
    
    return JsonResponse({
        'status': 'error',
        'message': 'Invalid request method.'
    })


def newsletter_confirm(request, token):
    subscriber = get_object_or_404(Newsletter, confirmation_token=token)
    
    if not subscriber.confirmed:
        subscriber.confirmed = True
        subscriber.save()
        messages.success(request, 'Your subscription has been confirmed. Thank you for subscribing!')
    else:
        messages.info(request, 'Your subscription was already confirmed.')
    
    return redirect('blog:blog_list')


def send_confirmation_email(subscriber):
    """Helper function to send confirmation email"""
    confirmation_link = f"{settings.SITE_URL}{reverse('blog:newsletter_confirm', args=[subscriber.confirmation_token])}"
    
    subject = 'Confirm Your Newsletter Subscription'
    message = f'''
Hello,

Thank you for subscribing to the Aaradhyadhrma newsletter!

Please confirm your subscription by clicking the link below:
{confirmation_link}

If you did not request this subscription, you can safely ignore this email.

Best regards,
The Aaradhyadhrma Team
    '''
    
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [subscriber.email]
    
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
