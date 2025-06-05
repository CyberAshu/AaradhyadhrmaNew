from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import TeamMember, Testimonial, ContactMessage
from .forms import ContactForm

def home(request):
    # Get featured testimonials for homepage
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-date_added')[:3]
    
    # Get featured team members for homepage
    team_members = TeamMember.objects.filter(is_active=True)[:4]
    
    # Define technologies we work with
    tech_stack = [
        {'name': 'Python', 'icon': 'fab fa-python'},
        {'name': 'Java', 'icon': 'fab fa-java'},
        {'name': 'JavaScript', 'icon': 'fab fa-js'},
        {'name': 'React', 'icon': 'fab fa-react'},
        {'name': 'Node.js', 'icon': 'fab fa-node-js'},
        {'name': 'HTML5', 'icon': 'fab fa-html5'},
        {'name': 'CSS3', 'icon': 'fab fa-css3-alt'},
        {'name': 'Sass', 'icon': 'fab fa-sass'},
        {'name': 'Bootstrap', 'icon': 'fab fa-bootstrap'},
        {'name': 'Angular', 'icon': 'fab fa-angular'},
        {'name': 'AWS', 'icon': 'fab fa-aws'},
        {'name': 'Docker', 'icon': 'fab fa-docker'}
    ]
    
    # Define services for homepage
    services = [
        {
            'title': 'Custom Software Development',
            'description': 'Tailor-made software solutions designed to meet your specific business needs.',
            'icon': 'fas fa-laptop-code'
        },
        {
            'title': 'AI/ML & Generative AI',
            'description': 'Cutting-edge artificial intelligence and machine learning solutions to transform your business.',
            'icon': 'fas fa-brain'
        },
        {
            'title': 'Full-stack Development',
            'description': 'End-to-end web and mobile application development with modern technologies.',
            'icon': 'fas fa-layer-group'
        },
        {
            'title': 'Technology Consultancy',
            'description': 'Expert advice and guidance on technology strategy, architecture, and implementation.',
            'icon': 'fas fa-chalkboard-teacher'
        }
    ]
    
    context = {
        'page_title': 'Aaradhyadhrma - Ancient Wisdom, Modern Solution',
        'meta_description': 'Aaradhyadhrma combines ancient wisdom with modern solutions to deliver innovative software, AI/ML, and technology consulting services.',
        'meta_keywords': 'software development, AI, ML, generative AI, full-stack development, technology consulting',
        'og_title': 'Aaradhyadhrma - Custom Software Development & AI Solutions',
        'og_description': 'We create tailor-made software solutions powered by AI/ML and cutting-edge technologies.',
        'testimonials': testimonials,
        'team_members': team_members,
        'tech_stack': tech_stack,
        'services': services,
    }
    return render(request, 'core/home.html', context)

def about(request):
    # Get all team members for about page
    team_members = TeamMember.objects.filter(is_active=True)
    
    # Company values for about page
    values = [
        {
            'title': 'Excellence',
            'description': 'We pursue excellence in everything we do, from code quality to client interactions.',
            'icon': 'fas fa-award'
        },
        {
            'title': 'Innovation',
            'description': 'We constantly explore new technologies and approaches to solve complex problems.',
            'icon': 'fas fa-lightbulb'
        },
        {
            'title': 'Integrity',
            'description': 'We maintain the highest ethical standards and transparency in all our dealings.',
            'icon': 'fas fa-shield-alt'
        },
        {
            'title': 'Collaboration',
            'description': 'We believe in the power of teamwork and open communication.',
            'icon': 'fas fa-hands-helping'
        }
    ]
    
    # Timeline/milestones
    milestones = [
        {
            'year': '2020',
            'title': 'Founded',
            'description': 'Aaradhyadhrma was established with a vision to bridge ancient wisdom with modern technology.'
        },
        {
            'year': '2021',
            'title': 'First Major Project',
            'description': 'Successfully delivered our first enterprise-level custom software solution.'
        },
        {
            'year': '2022',
            'title': 'AI Division',
            'description': 'Launched our specialized AI/ML division to focus on intelligent solutions.'
        },
        {
            'year': '2023',
            'title': 'International Expansion',
            'description': 'Expanded our services to international clients across Europe and North America.'
        },
        {
            'year': '2024',
            'title': 'Generative AI Solutions',
            'description': 'Pioneered innovative generative AI solutions for various industry verticals.'
        }
    ]
    
    context = {
        'page_title': 'About Us - Aaradhyadhrma',
        'meta_description': 'Learn about Aaradhyadhrma, our journey, values, and the team behind our innovative technology solutions.',
        'meta_keywords': 'about us, technology company, software development team, Aaradhyadhrma history, company values',
        'og_title': 'About Aaradhyadhrma - Our Story, Values & Team',
        'og_description': 'Discover the story behind Aaradhyadhrma, our core values, and the passionate team driving our innovation.',
        'team_members': team_members,
        'values': values,
        'milestones': milestones
    }
    return render(request, 'core/about.html', context)

def services(request):
    # Detailed services information
    services = [
        {
            'title': 'Custom Software Development',
            'description': 'Tailor-made software solutions designed to meet your specific business needs.',
            'long_description': 'We create custom software solutions that are perfectly aligned with your business objectives. Our development process begins with a thorough understanding of your requirements, followed by meticulous planning, agile development, rigorous testing, and ongoing support.',
            'icon': 'fas fa-laptop-code',
            'features': [
                'Requirement analysis and solution design',
                'Frontend and backend development',
                'Database design and optimization',
                'API development and integration',
                'Quality assurance and testing',
                'Deployment and maintenance'
            ]
        },
        {
            'title': 'AI/ML & Generative AI',
            'description': 'Cutting-edge artificial intelligence and machine learning solutions to transform your business.',
            'long_description': 'Leverage the power of artificial intelligence and machine learning to gain insights, automate processes, and create innovative solutions. Our AI experts specialize in developing intelligent systems that can learn, adapt, and improve over time.',
            'icon': 'fas fa-brain',
            'features': [
                'Predictive analytics and forecasting',
                'Natural language processing',
                'Computer vision and image recognition',
                'Recommendation systems',
                'Generative AI applications',
                'AI strategy consulting'
            ]
        },
        {
            'title': 'Full-stack Development',
            'description': 'End-to-end web and mobile application development with modern technologies.',
            'long_description': 'We deliver comprehensive full-stack development services using the latest technologies and frameworks. Our experienced developers create responsive, user-friendly, and scalable applications that provide exceptional user experiences across all devices.',
            'icon': 'fas fa-layer-group',
            'features': [
                'Responsive web application development',
                'Progressive web apps (PWAs)',
                'Mobile app development (iOS & Android)',
                'Cross-platform development',
                'UI/UX design and implementation',
                'Performance optimization'
            ]
        },
        {
            'title': 'Technology Consultancy',
            'description': 'Expert advice and guidance on technology strategy, architecture, and implementation.',
            'long_description': 'Our technology consultancy services help businesses make informed decisions about their technology investments. We provide strategic guidance on technology selection, architecture design, implementation planning, and digital transformation initiatives.',
            'icon': 'fas fa-chalkboard-teacher',
            'features': [
                'Technology strategy development',
                'Architecture design and review',
                'Digital transformation roadmap',
                'Technology stack selection',
                'Legacy system modernization',
                'IT security assessment and planning'
            ]
        }
    ]
    
    # Development process steps
    process_steps = [
        {
            'number': '01',
            'title': 'Discovery',
            'description': 'We begin by understanding your business needs, goals, and challenges through in-depth consultations.',
            'icon': 'fas fa-search'
        },
        {
            'number': '02',
            'title': 'Planning',
            'description': 'Our team creates a detailed roadmap with timelines, resources, and deliverables for your project.',
            'icon': 'fas fa-map'
        },
        {
            'number': '03',
            'title': 'Design',
            'description': 'We design intuitive user interfaces and robust system architectures tailored to your requirements.',
            'icon': 'fas fa-pencil-ruler'
        },
        {
            'number': '04',
            'title': 'Development',
            'description': 'Our developers bring the designs to life using agile methodologies and modern technologies.',
            'icon': 'fas fa-code'
        },
        {
            'number': '05',
            'title': 'Testing',
            'description': 'Rigorous quality assurance ensures your solution is reliable, secure, and performs optimally.',
            'icon': 'fas fa-vial'
        },
        {
            'number': '06',
            'title': 'Deployment',
            'description': 'We deploy your solution to production environments and ensure smooth transitions.',
            'icon': 'fas fa-rocket'
        },
        {
            'number': '07',
            'title': 'Support',
            'description': 'Our team provides ongoing maintenance, updates, and enhancements to keep your solution running smoothly.',
            'icon': 'fas fa-headset'
        }
    ]
    
    context = {
        'page_title': 'Services - Aaradhyadhrma',
        'meta_description': 'Explore our comprehensive range of technology services including Custom Software Development, AI/ML Solutions, Full-stack Development, and Technology Consultancy.',
        'meta_keywords': 'software development services, AI/ML solutions, full-stack development, technology consultancy, custom software',
        'og_title': 'Our Services - Aaradhyadhrma',
        'og_description': 'Discover how our technology services can transform your business with custom software, AI solutions, and expert consultancy.',
        'services': services,
        'process_steps': process_steps
    }
    return render(request, 'core/services.html', context)

def team(request):
    # Get all team members
    team_members = TeamMember.objects.filter(is_active=True).order_by('order')
    
    # Company culture information
    culture_items = [
        {
            'title': 'Continuous Learning',
            'description': 'We encourage continuous professional development and knowledge sharing.',
            'icon': 'fas fa-book-reader'
        },
        {
            'title': 'Work-Life Balance',
            'description': 'We believe in maintaining a healthy balance between professional and personal life.',
            'icon': 'fas fa-balance-scale'
        },
        {
            'title': 'Innovation Culture',
            'description': 'We foster a culture of innovation where creative ideas are welcomed and explored.',
            'icon': 'fas fa-lightbulb'
        },
        {
            'title': 'Collaborative Environment',
            'description': 'We work together as a team, valuing diverse perspectives and open communication.',
            'icon': 'fas fa-users'
        }
    ]
    
    context = {
        'page_title': 'Our Team - Aaradhyadhrma',
        'meta_description': 'Meet the talented team behind Aaradhyadhrma. Our diverse professionals bring expertise in software development, AI/ML, and technology consulting.',
        'meta_keywords': 'tech team, software developers, AI experts, tech consultants, Aaradhyadhrma team',
        'og_title': 'Meet Our Team - Aaradhyadhrma',
        'og_description': 'Get to know the experts who drive innovation at Aaradhyadhrma with their passion for technology and excellence.',
        'team_members': team_members,
        'culture_items': culture_items
    }
    return render(request, 'core/team.html', context)

def team_member_detail(request, member_id):
    # Get the specific team member
    try:
        member = TeamMember.objects.get(id=member_id, is_active=True)
    except TeamMember.DoesNotExist:
        # Redirect to team page if member doesn't exist
        return redirect('core:team')
    
    # Get the member's skills and projects from the database
    skills = member.skills.all().order_by('order')
    projects = member.projects.all().order_by('order')
    
    # If no skills or projects exist yet, provide default ones
    if not skills.exists():
        # Create some default skills for display
        default_skills = [
            {'name': 'Python', 'level': 90},
            {'name': 'JavaScript', 'level': 85},
            {'name': 'React', 'level': 80},
            {'name': 'Django', 'level': 95},
            {'name': 'UI/UX Design', 'level': 75},
            {'name': 'Database Design', 'level': 85}
        ]
    else:
        default_skills = None
    
    if not projects.exists():
        # Create some default projects for display
        default_projects = [
            {
                'title': 'E-commerce Platform',
                'description': 'A full-featured online shopping platform with payment integration.',
                'tech_stack_list': ['Python', 'Django', 'React', 'PostgreSQL']
            },
            {
                'title': 'Mobile Banking App',
                'description': 'Secure banking application with biometric authentication.',
                'tech_stack_list': ['Flutter', 'Firebase', 'Node.js']
            },
            {
                'title': 'AI-powered Analytics Dashboard',
                'description': 'Business intelligence tool with predictive analytics capabilities.',
                'tech_stack_list': ['Python', 'TensorFlow', 'Vue.js', 'MongoDB']
            }
        ]
    else:
        default_projects = None
    
    context = {
        'page_title': f'{member.name} - Team Member Profile - Aaradhyadhrma',
        'meta_description': f'Learn more about {member.name}, {member.position} at Aaradhyadhrma. Explore their expertise, projects, and professional background.',
        'meta_keywords': f'{member.name}, team member, {member.position}, professional profile, Aaradhyadhrma team',
        'og_title': f'{member.name} - Professional Profile',
        'og_description': f'Get to know {member.name}, our talented {member.position} at Aaradhyadhrma.',
        'member': member,
        'projects': projects,
        'skills': skills,
        'default_skills': default_skills,
        'default_projects': default_projects
    }
    return render(request, 'core/team_member_detail.html', context)

def testimonials(request):
    # Get all testimonials
    testimonials = Testimonial.objects.filter(is_active=True).order_by('-date_added')
    
    # Video testimonials (sample data - in a real app, this might come from a model)
    video_testimonials = [
        {
            'client_name': 'John Smith',
            'client_company': 'TechCorp Inc.',
            'client_position': 'CTO',
            'video_id': 'dQw4w9WgXcQ',  # YouTube video ID (placeholder)
            'thumbnail': 'testimonial-video-1.jpg',
            'brief': 'How Aaradhyadhrma helped TechCorp transform their legacy systems.'
        },
        {
            'client_name': 'Sophia Rodriguez',
            'client_company': 'FinanceHub',
            'client_position': 'Head of Innovation',
            'video_id': 'dQw4w9WgXcQ',  # YouTube video ID (placeholder)
            'thumbnail': 'testimonial-video-2.jpg',
            'brief': 'Implementing AI solutions that increased operational efficiency by 40%.'
        },
        {
            'client_name': 'Michael Chen',
            'client_company': 'GlobalRetail',
            'client_position': 'Digital Transformation Lead',
            'video_id': 'dQw4w9WgXcQ',  # YouTube video ID (placeholder)
            'thumbnail': 'testimonial-video-3.jpg',
            'brief': 'Our experience working with Aaradhyadhrma on our e-commerce platform.'
        }
    ]
    
    # Client logos for testimonials page
    context = {
        'page_title': 'Client Testimonials | Aaradhyadhrma',
        'meta_description': 'Read what our clients have to say about our services and solutions. Discover why clients trust Aaradhyadhrma for their technology needs.',
        'meta_keywords': 'testimonials, client reviews, customer feedback, software development reviews',
        'og_title': 'Client Testimonials | Aaradhyadhrma',
        'og_description': 'See what our satisfied clients have to say about our services and solutions.',
        'testimonials': testimonials,
    }
    
    return render(request, 'core/testimonials.html', context)


def offline(request):
    """
    Offline Page View
    """
    context = {
        'page_title': 'Offline | Aaradhyadhrma',
        'meta_description': 'You are currently offline. Please check your internet connection.',
        'meta_keywords': 'offline, no connection, Aaradhyadhrma',
        'og_title': 'Offline | Aaradhyadhrma',
        'og_description': 'You are currently offline. Please check your internet connection.',
    }
    
    return render(request, 'offline.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save the contact message
            contact = form.save(commit=False)
            contact.ip_address = request.META.get('REMOTE_ADDR', '')
            contact.user_agent = request.META.get('HTTP_USER_AGENT', '')
            contact.save()
            
            # Send notification email (commented out as email configuration might be missing)
            # send_mail(
            #     subject=f'New contact message from {contact.name}',
            #     message=f'Name: {contact.name}\nEmail: {contact.email}\nPhone: {contact.phone}\nMessage: {contact.message}',
            #     from_email='noreply@aaradhyadhrma.com',
            #     recipient_list=['contact@aaradhyadhrma.com'],
            #     fail_silently=False,
            # )
            
            messages.success(request, 'Your message has been sent successfully! We will get back to you shortly.')
            return redirect('core:contact')
        else:
            messages.error(request, 'There was an error with your submission. Please check the form and try again.')
    else:
        form = ContactForm()
    
    # Office locations
    offices = [
        {
            'name': 'Headquarters',
            'address': '123 Tech Park, Electronic City Phase 1, Indore, Karnataka 560100, India',
            'phone': '+91 80 1234 5678',
            'email': 'info@aaradhyadhrma.com',
            'hours': 'Monday - Friday: 9:00 AM - 6:00 PM',
            'map_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15555.515435625248!2d77.6400805!3d12.8399376!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3bae6b2ef7a36b7d%3A0xb746b0c8cb547eec!2sElectronic%20City%20Phase%201%2C%20Electronic%20City%2C%20Bengaluru%2C%20Karnataka!5e0!3m2!1sen!2sin!4v1622619115934!5m2!1sen!2sin'
        },
        {
            'name': 'Mumbai Office',
            'address': '456 Business Tower, Andheri East, Mumbai, Maharashtra 400069, India',
            'phone': '+91 22 9876 5432',
            'email': 'mumbai@aaradhyadhrma.com',
            'hours': 'Monday - Friday: 9:00 AM - 6:00 PM',
            'map_url': 'https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d15078.427232889629!2d72.85333620000001!3d19.1137711!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3be7c83fd8e64e3f%3A0x4438b7039e9a379b!2sAndheri%20East%2C%20Mumbai%2C%20Maharashtra!5e0!3m2!1sen!2sin!4v1622619168903!5m2!1sen!2sin'
        },
    ]
    
    # FAQ items for contact page
    faqs = [
        {
            'question': 'How do I request a quote for my project?',
            'answer': 'You can request a quote by filling out our contact form with details about your project requirements. Our team will get back to you within 24-48 hours with an initial assessment and follow-up questions if needed.'
        },
        {
            'question': 'What information should I provide for a project inquiry?',
            'answer': 'To help us understand your project better, please include details about your project goals, target audience, desired features, timeline, and budget range. The more information you provide, the more accurate our initial assessment will be.'
        },
        {
            'question': 'How long does it typically take to complete a project?',
            'answer': 'Project timelines vary based on complexity, scope, and requirements. A simple website might take 4-6 weeks, while complex enterprise applications can take several months. We\'ll provide a detailed timeline estimate during our proposal phase.'
        },
        {
            'question': 'Do you provide ongoing support after project completion?',
            'answer': 'Yes, we offer various maintenance and support packages to ensure your application continues to run smoothly after launch. These can include regular updates, security patches, performance monitoring, and feature enhancements.'
        },
    ]
    
    context = {
        'page_title': 'Contact Us - Aaradhyadhrma',
        'meta_description': 'Get in touch with Aaradhyadhrma for your software development, AI/ML solutions, and technology consulting needs. We\'re here to help transform your ideas into reality.',
        'meta_keywords': 'contact us, software development inquiry, technology consulting, get in touch, project quote',
        'og_title': 'Contact Aaradhyadhrma - Get in Touch',
        'og_description': 'Reach out to our team for inquiries about custom software development, AI/ML solutions, and technology consulting services.',
        'form': form,
        'offices': offices,
        'faqs': faqs
    }
    return render(request, 'core/contact.html', context)


def case_study(request, slug):
    """View function for displaying case studies"""
    
    # Define case studies data (in a real application, this would come from a database)
    case_studies = {
        'e-commerce-platform-redesign': {
            'title': 'E-Commerce Platform Redesign',
            'client': 'Global Retail Solutions',
            'industry': 'Retail',
            'duration': '4 months',
            'year': '2024',
            'challenge': "The client's existing e-commerce platform was outdated, had poor user experience, and was experiencing declining conversion rates. They needed a complete redesign that would improve user engagement and increase sales.",
            'solution': 'We conducted extensive user research and competitive analysis to identify pain points and opportunities. Our team then redesigned the entire platform with a focus on intuitive navigation, mobile responsiveness, and streamlined checkout process. We implemented advanced product filtering, personalized recommendations, and integrated a robust analytics system.',
            'results': [
                '45% increase in conversion rates',
                '30% reduction in cart abandonment',
                '60% improvement in mobile engagement',
                '25% increase in average order value'
            ],
            'technologies': ['React', 'Node.js', 'MongoDB', 'AWS', 'Elasticsearch'],
            'testimonial': {
                'quote': 'The redesigned platform has transformed our business. The user experience is exceptional, and the results speak for themselves with significant improvements in all our key metrics.',
                'author': 'Rajiv Patel',
                'position': 'Director, Global Retail Solutions'
            },
            'image': 'images/case-study-1.png'
        },
        'ai-powered-analytics-dashboard': {
            'title': 'AI-Powered Analytics Dashboard',
            'client': 'DataViz Solutions',
            'industry': 'Data Science',
            'duration': '6 months',
            'year': '2023',
            'challenge': 'The client was struggling to make sense of the vast amounts of data they were collecting. They needed an intuitive dashboard that could process complex data sets and present actionable insights in real-time.',
            'solution': 'We developed a custom AI-powered analytics dashboard that uses machine learning algorithms to process and analyze data from multiple sources. The solution includes predictive analytics capabilities, automated reporting, and customizable visualization tools.',
            'results': [
                '70% reduction in data analysis time',
                '40% improvement in prediction accuracy',
                '50% increase in identified business opportunities',
                '35% cost savings in data processing'
            ],
            'technologies': ['Python', 'TensorFlow', 'React', 'PostgreSQL', 'Docker', 'Google Cloud'],
            'testimonial': {
                'quote': 'The AI-powered dashboard has revolutionized how we process and visualize data. We can now make data-driven decisions faster and with greater confidence.',
                'author': 'Ananya Gupta',
                'position': 'Head of Data Science, DataViz Solutions'
            },
            'image': 'images/case-study-2.png'
        },
        'enterprise-resource-planning-system': {
            'title': 'Enterprise Resource Planning System',
            'client': 'Manufacturing Excellence',
            'industry': 'Manufacturing',
            'duration': '8 months',
            'year': '2023',
            'challenge': 'The client was using multiple disconnected systems to manage their operations, leading to inefficiencies, data inconsistencies, and difficulty in tracking key performance indicators.',
            'solution': 'We developed a comprehensive ERP solution that integrated all aspects of their business including inventory management, production planning, supply chain management, and financial reporting. The system features real-time dashboards, automated workflows, and mobile access for field staff.',
            'results': [
                '35% improvement in operational efficiency',
                '25% reduction in inventory costs',
                '40% faster order fulfillment',
                '20% increase in production capacity'
            ],
            'technologies': ['Java', 'Spring Boot', 'Angular', 'Oracle Database', 'Kubernetes'],
            'testimonial': {
                'quote': 'The custom ERP system has transformed our operations. We now have complete visibility across all departments and can make informed decisions based on real-time data.',
                'author': 'Vikram Singh',
                'position': 'CIO, Manufacturing Excellence'
            },
            'image': 'images/case-study-3.png'
        }
    }
    
    # Get the case study data or return a 404 if not found
    case_study_data = case_studies.get(slug)
    if not case_study_data:
        # In a real application, you might want to use Django's get_object_or_404
        # For now, we'll just redirect to testimonials page if the case study doesn't exist
        messages.error(request, 'The requested case study does not exist.')
        return redirect('core:testimonials')
    
    context = {
        'case_study': case_study_data,
        'title': f'Case Study: {case_study_data["title"]}',
        'meta_description': f'Learn how Aaradhyadhrma helped {case_study_data["client"]} achieve success through innovative technology solutions.'
    }
    
    return render(request, 'core/case_study.html', context)
