#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'aaradhyadhrma.settings')
django.setup()

from core.models import QuickReplyTemplate

def create_default_templates():
    """Create default quick reply templates"""
    
    templates = [
        {
            'name': 'General Acknowledgment',
            'template_type': 'general',
            'subject': 'Thank you for contacting us',
            'message': '''Dear {name},

Thank you for reaching out to us. We have received your message and will get back to you within 24-48 hours.

If your inquiry is urgent, please feel free to call us at our support line.

Best regards,
The Aaradhyadhrma Team'''
        },
        {
            'name': 'Reseller Information',
            'template_type': 'reseller',
            'subject': 'Information about our reseller program',
            'message': '''Dear {name},

Thank you for your interest in our reseller program.

We offer competitive pricing and comprehensive support for our authorized resellers. Our team will contact you within 2 business days to discuss the partnership opportunities and requirements.

In the meantime, you can review our reseller guidelines on our website.

Best regards,
Partnership Team
Aaradhyadhrma'''
        },
        {
            'name': 'Support Request Acknowledgment',
            'template_type': 'support',
            'subject': 'Your support request has been received',
            'message': '''Dear {name},

We have received your support request and our technical team is reviewing it.

Expected response time: 4-6 hours during business days

For immediate assistance, please check our knowledge base on our website or contact our support hotline.

Thank you for your patience.

Best regards,
Support Team
Aaradhyadhrma'''
        },
        {
            'name': 'Follow-up Required',
            'template_type': 'custom',
            'subject': 'Additional information needed',
            'message': '''Dear {name},

Thank you for contacting us. To better assist you, we need some additional information:

• Please specify your requirements in more detail
• Let us know your preferred timeline
• Any specific preferences or constraints

Please reply to this email with the requested information, and we will get back to you promptly.

Best regards,
The Aaradhyadhrma Team'''
        }
    ]
    
    created_count = 0
    for template_data in templates:
        template, created = QuickReplyTemplate.objects.get_or_create(
            name=template_data['name'],
            defaults=template_data
        )
        if created:
            created_count += 1
            print(f"Created template: {template.name}")
        else:
            print(f"Template already exists: {template.name}")
    
    print(f"\nCreated {created_count} new templates.")
    print(f"Total templates: {QuickReplyTemplate.objects.count()}")

if __name__ == '__main__':
    create_default_templates()
