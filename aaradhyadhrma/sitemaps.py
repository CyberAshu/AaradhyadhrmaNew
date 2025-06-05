from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post
from careers.models import Job


class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:about', 'core:services', 
                'core:team', 'core:testimonials', 'core:contact',
                'blog:blog_list', 'careers:careers_list']

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return Post.objects.filter(status='published')

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('blog:blog_detail', args=[obj.slug])


class JobSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return Job.objects.filter(is_active=True)

    def lastmod(self, obj):
        return obj.updated_at

    def location(self, obj):
        return reverse('careers:job_detail', args=[obj.slug])
