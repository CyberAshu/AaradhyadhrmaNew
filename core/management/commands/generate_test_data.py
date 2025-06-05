from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from django.db import transaction
import random
import datetime
import os
from django.conf import settings

from core.models import TeamMember, Testimonial
from blog.models import Category, Tag, Post, Comment
from careers.models import Job

class Command(BaseCommand):
    help = 'Generates test data for the Aaradhyadhrma website'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Delete existing data before creating new data',
        )

    def handle(self, *args, **kwargs):
        # Clear existing data if --flush is specified
        if kwargs['flush']:
            self.stdout.write(self.style.WARNING('Deleting existing data...'))
            self._flush_data()
            
        self.stdout.write(self.style.SUCCESS('Starting test data generation...'))
        
        # Create a superuser if one doesn't exist
        self._create_superuser()
        
        # Generate team members
        self._generate_team_members()
        
        # Generate testimonials
        self._generate_testimonials()
        
        # Generate blog content
        self._generate_blog_content()
        
        # Generate job listings
        self._generate_job_listings()
        
        self.stdout.write(self.style.SUCCESS('Test data generation completed successfully!'))

    def _flush_data(self):
        """Delete all existing data"""
        TeamMember.objects.all().delete()
        Testimonial.objects.all().delete()
        Comment.objects.all().delete()
        Post.objects.all().delete()
        Tag.objects.all().delete()
        Category.objects.all().delete()
        Job.objects.all().delete()
        # Don't delete users - keep admin user

    def _create_superuser(self):
        """Create a superuser if one doesn't exist"""
        if not User.objects.filter(is_superuser=True).exists():
            User.objects.create_superuser(
                'admin',
                'admin@example.com',
                'adminpassword'
            )
            self.stdout.write(self.style.SUCCESS('Superuser created'))
        else:
            self.stdout.write(self.style.SUCCESS('Superuser already exists'))
            
    def _generate_team_members(self):
        """Generate team members"""
        self.stdout.write('Generating team members...')
        
        team_members_data = [
            {
                'name': 'Ayush Sharma',
                'position': 'CEO & Founder',
                'bio': 'Ayush is the founder and CEO of Aaradhyadhrma, with over 15 years of experience in software development and AI/ML technologies. He has led numerous successful projects for Fortune 500 companies and startups alike.',
                'linkedin': 'https://linkedin.com/',
                'github': 'https://github.com/',
                'twitter': 'https://twitter.com/',
                'order': 1,
            },
            {
                'name': 'Ashutosh Patel',
                'position': 'CTO',
                'bio': 'Ashutosh is an experienced technology leader with expertise in architecture design, cloud infrastructure, and emerging technologies. He oversees the technical direction of all client projects.',
                'linkedin': 'https://linkedin.com/',
                'github': 'https://github.com/',
                'twitter': 'https://twitter.com/',
                'order': 2,
            },
            {
                'name': 'Rahul Singh',
                'position': 'Lead AI Engineer',
                'bio': 'Rahul specializes in machine learning and artificial intelligence solutions. He has implemented cutting-edge AI systems across various industries including healthcare, finance, and e-commerce.',
                'linkedin': 'https://linkedin.com/',
                'github': 'https://github.com/',
                'order': 3,
            },
            {
                'name': 'Priya Sharma',
                'position': 'UX/UI Design Lead',
                'bio': 'Priya leads our design team with a focus on creating intuitive, accessible, and engaging user experiences. She has a background in human-computer interaction and visual design.',
                'linkedin': 'https://linkedin.com/',
                'twitter': 'https://twitter.com/',
                'order': 4,
            },
            {
                'name': 'Vikram Reddy',
                'position': 'Full-stack Developer',
                'bio': 'Vikram is an experienced full-stack developer proficient in multiple programming languages and frameworks. He specializes in building scalable web applications.',
                'github': 'https://github.com/',
                'order': 5,
            },
        ]
        
        for member_data in team_members_data:
            # Use SVG images we've already created
            photo_path = member_data.get('name').split()[0].lower()
            
            TeamMember.objects.create(
                name=member_data['name'],
                position=member_data['position'],
                bio=member_data['bio'],
                photo=f'team/{photo_path}.svg',  # Using SVG images we created earlier
                linkedin=member_data.get('linkedin', ''),
                github=member_data.get('github', ''),
                twitter=member_data.get('twitter', ''),
                order=member_data['order'],
                is_active=True
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(team_members_data)} team members'))
    
    def _generate_testimonials(self):
        """Generate client testimonials"""
        self.stdout.write('Generating testimonials...')
        
        testimonials_data = [
            {
                'name': 'Sanjay Mehta',
                'position': 'CTO',
                'company': 'TechInnovate Solutions',
                'comment': 'Aaradhyadhrma delivered exceptional software solutions that transformed our business operations. Their expertise in AI/ML technologies helped us gain valuable insights from our data, leading to better decision-making and increased efficiency.',
                'rating': 5,
            },
            {
                'name': 'Priya Sharma',
                'position': 'CEO',
                'company': 'InnoTech Enterprises',
                'comment': 'Working with Aaradhyadhrma has been a game-changer for our organization. Their team\'s deep technical knowledge and commitment to quality resulted in a custom software solution that exceeded our expectations. I highly recommend their services.',
                'rating': 5,
            },
            {
                'name': 'Rajiv Patel',
                'position': 'Director',
                'company': 'Global Retail Solutions',
                'comment': 'We partnered with Aaradhyadhrma for our e-commerce platform redesign, and they delivered a solution that not only looks great but also significantly improved our conversion rates. Their attention to detail and focus on user experience was impressive.',
                'rating': 4,
            },
            {
                'name': 'Meera Khan',
                'position': 'Head of Digital Transformation',
                'company': 'FinanceHub',
                'comment': 'The AI solution developed by Aaradhyadhrma helped us automate our document processing workflow, reducing processing time by 70% and significantly decreasing errors. Their team took the time to understand our specific needs and delivered a tailored solution.',
                'rating': 5,
            },
            {
                'name': 'Vikram Joshi',
                'position': 'Product Manager',
                'company': 'HealthTech Innovations',
                'comment': 'Aaradhyadhrma\'s development team integrated seamlessly with our in-house staff, enhancing our capabilities and helping us meet tight deadlines. Their technical expertise and collaborative approach made them a valuable partner.',
                'rating': 4,
            },
        ]
        
        for idx, testimonial_data in enumerate(testimonials_data):
            created_date = timezone.now() - datetime.timedelta(days=random.randint(1, 90))
            
            Testimonial.objects.create(
                name=testimonial_data['name'],
                position=testimonial_data['position'],
                company=testimonial_data['company'],
                comment=testimonial_data['comment'],
                rating=testimonial_data['rating'],
                # No photo, using placeholder in template
                is_active=True,
                date_added=created_date
            )
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(testimonials_data)} testimonials'))

    def _generate_blog_content(self):
        """Generate blog categories, tags, posts, and comments"""
        self.stdout.write('Generating blog content...')
        
        # Create blog categories
        categories = [
            {'name': 'Technology Trends', 'description': 'Latest developments in technology and innovation'},
            {'name': 'Software Development', 'description': 'Best practices, tips, and insights in software development'},
            {'name': 'AI & Machine Learning', 'description': 'Advancements and applications in AI and machine learning'},
            {'name': 'Business Insights', 'description': 'Strategic advice for technology-driven businesses'},
            {'name': 'Case Studies', 'description': 'Real-world examples of successful projects'},
        ]
        
        created_categories = []
        for category_data in categories:
            category = Category.objects.create(
                name=category_data['name'],
                slug=slugify(category_data['name']),
                description=category_data['description']
            )
            created_categories.append(category)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_categories)} blog categories'))
        
        # Create tags
        tags = [
            'Python', 'Django', 'React', 'JavaScript', 'AI', 'Machine Learning',
            'Web Development', 'API', 'Cloud', 'DevOps', 'UI/UX', 'Data Science',
            'Blockchain', 'IoT', 'Mobile Development', 'Security', 'Testing',
            'Agile', 'Microservices', 'Docker', 'Kubernetes'
        ]
        
        created_tags = []
        for tag_name in tags:
            tag = Tag.objects.create(
                name=tag_name,
                slug=slugify(tag_name)
            )
            created_tags.append(tag)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_tags)} blog tags'))
        
        # Create users for blog authors
        authors = []
        if not User.objects.filter(username='author1').exists():
            author1 = User.objects.create_user(
                username='author1',
                email='author1@example.com',
                password='password123',
                first_name='John',
                last_name='Smith'
            )
            authors.append(author1)
        else:
            authors.append(User.objects.get(username='author1'))
            
        if not User.objects.filter(username='author2').exists():
            author2 = User.objects.create_user(
                username='author2',
                email='author2@example.com',
                password='password123',
                first_name='Emily',
                last_name='Johnson'
            )
            authors.append(author2)
        else:
            authors.append(User.objects.get(username='author2'))
            
        # Add admin as an author too
        authors.append(User.objects.get(username='admin'))
        
        # Create blog posts
        blog_posts = [
            {
                'title': 'The Future of AI in Business',
                'excerpt': 'Explore how artificial intelligence is transforming business operations and decision-making processes.',
                'content': 'Artificial intelligence is revolutionizing how businesses operate, from automating routine tasks to providing deep insights from data analysis. In this article, we explore the current and future applications of AI across various industries.\n\nMany organizations are already using AI to improve customer service through chatbots, optimize supply chains through predictive analytics, and enhance marketing campaigns through personalization. The technology continues to evolve rapidly, with new capabilities emerging regularly.\n\nHowever, implementing AI successfully requires careful planning, quality data, and the right expertise. Companies need to consider ethical implications and ensure transparency in their AI systems.\n\nAs we look to the future, AI will become increasingly integrated into business operations, enabling more efficient processes and innovative products and services. Organizations that embrace this technology thoughtfully will gain significant competitive advantages.',
                'category': 'AI & Machine Learning',
                'tags': ['AI', 'Machine Learning', 'Business Insights'],
                'status': 'published',
            },
            {
                'title': 'Best Practices for Modern Web Development',
                'excerpt': 'Key principles and practices for building robust, scalable web applications in today\'s technology landscape.',
                'content': 'The web development landscape continues to evolve rapidly, with new frameworks, tools, and best practices emerging regularly. This article outlines key principles for modern web development that will help you build robust, maintainable applications.\n\nOne of the most important practices is adopting a component-based architecture, which improves code reusability and maintenance. Frameworks like React, Vue, and Angular facilitate this approach by providing powerful component models.\n\nAnother critical aspect is performance optimization. Techniques like code splitting, lazy loading, and proper asset optimization can significantly improve load times and user experience. Additionally, implementing progressive web app (PWA) features can enhance offline capabilities and mobile experience.\n\nSecurity should never be an afterthought. Regular dependency updates, input validation, proper authentication and authorization, and protection against common vulnerabilities are essential practices.\n\nFinally, a robust testing strategy, including unit tests, integration tests, and end-to-end tests, ensures that your application functions correctly and continues to do so as you make changes.',
                'category': 'Software Development',
                'tags': ['Web Development', 'JavaScript', 'React', 'Testing'],
                'status': 'published',
            },
            {
                'title': 'How We Implemented a Real-time Analytics Dashboard',
                'excerpt': 'A case study on how we built a high-performance real-time analytics dashboard for a financial services client.',
                'content': 'In this case study, we share our experience developing a real-time analytics dashboard for a major financial services provider. The client needed a solution that could process millions of transactions daily and provide instant insights to their analysts.\n\nThe Challenge:\nThe client\'s existing system had significant latency issues, with data updates taking up to 30 minutes to appear on dashboards. This delay was impacting decision-making and preventing timely responses to potential fraud cases.\n\nOur Approach:\nWe implemented a microservices architecture using Node.js for the backend API services and React for the frontend dashboard. To handle real-time data processing, we utilized Apache Kafka for message queuing and Redis for caching frequently accessed data.\n\nThe solution included customizable dashboards with drag-and-drop widgets, allowing users to configure their views based on their specific needs. We also implemented advanced filtering capabilities and configurable alerts.\n\nResults:\nThe new system reduced data update latency from 30 minutes to under 2 seconds, allowing analysts to identify and respond to issues in real-time. The intuitive interface decreased training time for new users by 60%, and the overall efficiency of the fraud detection team improved by 35%.',
                'category': 'Case Studies',
                'tags': ['Dashboard', 'React', 'Microservices', 'Redis'],
                'status': 'published',
            },
            {
                'title': 'Containerization with Docker: A Beginner\'s Guide',
                'excerpt': 'Learn the basics of containerization and how to use Docker to simplify your development and deployment processes.',
                'content': 'Containerization has transformed how we develop, test, and deploy applications. This beginner\'s guide introduces Docker and explains how containers can streamline your workflow.\n\nWhat is Docker?\nDocker is a platform that enables developers to build, ship, and run applications in containers. Containers package an application with all its dependencies, ensuring consistent behavior across different environments.\n\nKey Benefits:\n- Consistency: Eliminates "it works on my machine" problems\n- Isolation: Applications run in their own environment without interfering with each other\n- Portability: Containers can run on any system that supports Docker\n- Efficiency: Containers share the host OS kernel, making them lighter than virtual machines\n\nGetting Started:\nThis article walks through installing Docker, understanding basic concepts like images and containers, and creating your first Dockerfile. We\'ll also cover essential commands for managing containers and images.\n\nReal-World Usage:\nFinally, we\'ll explore common use cases for Docker in development workflows, including local development environments, continuous integration, and deployment strategies.',
                'category': 'Software Development',
                'tags': ['Docker', 'DevOps', 'Containerization'],
                'status': 'published',
            },
            {
                'title': 'The Rise of Large Language Models',
                'excerpt': 'Exploring the rapid evolution of large language models and their impact on various industries.',
                'content': 'Large Language Models (LLMs) like GPT-4, Claude, and Llama have emerged as powerful tools capable of understanding and generating human-like text. This article explores their rapid evolution and growing impact across industries.\n\nLLMs represent a significant advancement in natural language processing, trained on vast amounts of text data to recognize patterns and generate coherent, contextually relevant content. Their capabilities extend beyond simple text generation to complex reasoning, translation, summarization, and even code generation.\n\nIndustry Applications:\n- Customer Service: Enhancing chatbots and virtual assistants\n- Content Creation: Assisting with writing, editing, and creative processes\n- Healthcare: Summarizing medical literature and assisting with documentation\n- Education: Personalized tutoring and content development\n- Software Development: Code generation, debugging, and documentation\n\nChallenges and Considerations:\nDespite their capabilities, LLMs face challenges including bias, hallucinations (generating plausible but incorrect information), and ethical considerations around content generation. Organizations implementing these technologies must establish appropriate guardrails and human oversight.\n\nThe Future Outlook:\nAs research continues, we anticipate more specialized models, improved reasoning capabilities, and better multimodal integration. The most successful implementations will likely combine LLMs with other AI techniques and human expertise to create truly transformative solutions.',
                'category': 'AI & Machine Learning',
                'tags': ['AI', 'Machine Learning', 'Natural Language Processing'],
                'status': 'published',
            },
        ]
        
        created_posts = []
        for post_data in blog_posts:
            # Find the appropriate category
            category = next((cat for cat in created_categories if cat.name == post_data['category']), created_categories[0])
            
            # Create the post
            post = Post.objects.create(
                title=post_data['title'],
                slug=slugify(post_data['title']),
                author=random.choice(authors),
                content=post_data['content'],
                excerpt=post_data['excerpt'],
                category=category,
                status=post_data['status'],
                published_on=timezone.now() - datetime.timedelta(days=random.randint(1, 60))
            )
            
            # Add tags
            for tag_name in post_data['tags']:
                matching_tags = [t for t in created_tags if t.name == tag_name]
                if matching_tags:
                    post.tags.add(matching_tags[0])
                else:
                    # Create the tag if it doesn't exist
                    new_tag = Tag.objects.create(name=tag_name, slug=slugify(tag_name))
                    post.tags.add(new_tag)
                    created_tags.append(new_tag)
            
            created_posts.append(post)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_posts)} blog posts'))
        
        # Create comments for blog posts
        commenters = [
            {'name': 'Michael Brown', 'email': 'michael@example.com'},
            {'name': 'Sarah Jones', 'email': 'sarah@example.com'},
            {'name': 'David Wilson', 'email': 'david@example.com'},
            {'name': 'Jennifer Lee', 'email': 'jennifer@example.com'},
            {'name': 'Robert Chen', 'email': 'robert@example.com'},
        ]
        
        comments_count = 0
        for post in created_posts:
            # Each post gets 1-3 comments
            num_comments = random.randint(1, 3)
            for _ in range(num_comments):
                commenter = random.choice(commenters)
                comment_text = random.choice([
                    "Great article! Thanks for sharing these insights.",
                    "This is exactly what I've been looking for. Very helpful information.",
                    "I've been working with these technologies and your points are spot on.",
                    "Interesting perspective. Have you considered the implications for smaller businesses?",
                    "Well-written and informative. Looking forward to more content like this."
                ])
                
                Comment.objects.create(
                    post=post,
                    name=commenter['name'],
                    email=commenter['email'],
                    body=comment_text,
                    created_on=timezone.now() - datetime.timedelta(days=random.randint(0, 30)),
                    active=True
                )
                comments_count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Created {comments_count} blog comments'))

    def _generate_job_listings(self):
        """Generate job listings"""
        self.stdout.write('Generating job listings...')
        
        job_listings = [
            {
                'title': 'Senior Full-stack Developer',
                'location': 'Indore, India',
                'employment_type': 'full_time',
                'description': 'We are looking for an experienced Full-stack Developer to join our growing team. The ideal candidate will be responsible for developing and maintaining both frontend and backend components of our web applications.',
                'responsibilities': '- Design and develop high-quality web applications using modern frameworks\n- Write clean, maintainable, and efficient code\n- Collaborate with cross-functional teams to define and implement new features\n- Troubleshoot and debug applications\n- Optimize applications for maximum speed and scalability\n- Stay up-to-date with emerging trends and technologies',
                'requirements': '- 5+ years of experience in full-stack development\n- Proficiency in JavaScript, Python, and relevant frameworks (React, Django, etc.)\n- Experience with database design and optimization\n- Familiarity with front-end technologies (HTML5, CSS3)\n- Strong problem-solving skills and attention to detail\n- Excellent communication and teamwork abilities',
                'salary_range': '₹18-25 LPA, based on experience',
                'is_active': True,
                'closing_date': timezone.now() + datetime.timedelta(days=30),
            },
            {
                'title': 'AI/ML Engineer',
                'location': 'Indore, India (Remote option available)',
                'employment_type': 'full_time',
                'description': 'We are seeking a talented AI/ML Engineer to help develop innovative solutions for our clients. This role involves designing, implementing, and optimizing machine learning models and AI systems.',
                'responsibilities': '- Design and implement machine learning models to address business problems\n- Process, clean, and verify the integrity of data used for analysis\n- Train and retrain systems when necessary\n- Extend existing ML libraries and frameworks\n- Work closely with data engineers and software developers\n- Keep up with developments in the AI/ML field',
                'requirements': '- Masters or PhD in Computer Science, AI, or related field\n- 3+ years of experience in machine learning or AI development\n- Proficiency in Python and relevant ML libraries (TensorFlow, PyTorch, scikit-learn)\n- Experience with data visualization tools\n- Strong mathematical skills (linear algebra, calculus, statistics)\n- Excellent problem-solving and communication skills',
                'salary_range': '₹20-30 LPA, based on experience',
                'is_active': True,
                'closing_date': timezone.now() + datetime.timedelta(days=45),
            },
            {
                'title': 'UX/UI Designer',
                'location': 'Indore, India',
                'employment_type': 'full_time',
                'description': 'We are looking for a creative UX/UI Designer to create engaging and effective user experiences for our web and mobile applications. The ideal candidate will combine design thinking with technical knowledge to produce intuitive interfaces.',
                'responsibilities': '- Create user flows, wireframes, prototypes, and mockups\n- Design UI elements such as input controls, navigational components, and informational components\n- Develop UI mockups and prototypes that clearly illustrate how sites function and look\n- Create original graphic designs\n- Prepare and present rough drafts to internal teams and key stakeholders\n- Conduct user research and evaluate user feedback',
                'requirements': '- 3+ years of experience in UX/UI design\n- Proficiency in design tools such as Figma, Sketch, Adobe XD\n- Understanding of interaction design and information architecture\n- Knowledge of HTML/CSS/JavaScript is a plus\n- Strong portfolio showcasing design projects\n- Excellent visual design skills with sensitivity to user-system interaction',
                'salary_range': '₹12-18 LPA, based on experience',
                'is_active': True,
                'closing_date': timezone.now() + datetime.timedelta(days=30),
            },
            {
                'title': 'DevOps Engineer',
                'location': 'Remote',
                'employment_type': 'full_time',
                'description': 'We are seeking a skilled DevOps Engineer to help build and maintain our cloud infrastructure. This role involves automating processes, implementing CI/CD pipelines, and ensuring the reliability and scalability of our systems.',
                'responsibilities': '- Design and implement build, deployment, and configuration management\n- Set up tools and infrastructure for CI/CD pipelines\n- Build and maintain monitoring and alerting systems\n- Troubleshoot and resolve issues in development, testing, and production environments\n- Implement security and data protection solutions\n- Optimize infrastructure for performance and cost',
                'requirements': '- 4+ years of experience in DevOps or a similar role\n- Strong knowledge of cloud services (AWS, Azure, or GCP)\n- Experience with configuration management tools (Ansible, Chef, Puppet)\n- Proficiency with container technologies (Docker, Kubernetes)\n- Familiarity with infrastructure as code (Terraform, CloudFormation)\n- Scripting skills (Python, Bash)\n- Understanding of networking and security concepts',
                'salary_range': '₹15-25 LPA, based on experience',
                'is_active': True,
                'closing_date': timezone.now() + datetime.timedelta(days=60),
            },
            {
                'title': 'Product Manager - AI Solutions',
                'location': 'Indore, India (Hybrid)',
                'employment_type': 'full_time',
                'description': 'We are looking for a Product Manager to lead the development of our AI-based solutions. The ideal candidate will bridge the gap between technical and business teams, ensuring our products meet market needs and deliver value to customers.',
                'responsibilities': '- Define product vision, strategy, and roadmap for AI solutions\n- Gather and prioritize product requirements from stakeholders\n- Work closely with engineering teams to deliver features\n- Analyze market trends and competitor offerings\n- Define success metrics and monitor product performance\n- Communicate product value to internal and external stakeholders',
                'requirements': '- 5+ years of experience in product management, preferably with AI/ML products\n- Understanding of AI/ML concepts and technologies\n- Experience bringing technology products to market\n- Strong analytical and problem-solving skills\n- Excellent communication and presentation abilities\n- Technical background or MBA is a plus',
                'salary_range': '₹20-35 LPA, based on experience',
                'is_active': True,
                'closing_date': timezone.now() + datetime.timedelta(days=45),
            },
        ]
        
        created_jobs = []
        for job_data in job_listings:
            # Calculate posted date (between 1-15 days ago)
            posted_date = timezone.now() - datetime.timedelta(days=random.randint(1, 15))
            
            job = Job.objects.create(
                title=job_data['title'],
                slug=slugify(job_data['title']),
                location=job_data['location'],
                employment_type=job_data['employment_type'],
                description=job_data['description'],
                responsibilities=job_data['responsibilities'],
                requirements=job_data['requirements'],
                salary_range=job_data['salary_range'],
                is_active=job_data['is_active'],
                posted_date=posted_date,
                closing_date=job_data['closing_date'],
            )
            created_jobs.append(job)
        
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_jobs)} job listings'))

