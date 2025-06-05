import os
import json
import google.generativeai as genai
import logging
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Conversation, Message
from core.models import ContactForm
import uuid
from datetime import datetime

# Set up logging
logger = logging.getLogger('chatbot')
if not logger.handlers:
    # Create handlers
    file_handler = logging.FileHandler('chatbot.log')
    console_handler = logging.StreamHandler()
    
    # Create formatters
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
    
    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)

# Configure the Gemini API if key is available
GEMINI_ENABLED = hasattr(settings, 'GEMINI_API_KEY') and settings.GEMINI_API_KEY and settings.GEMINI_API_KEY != 'YOUR_GEMINI_API_KEY'

if GEMINI_ENABLED:
    genai.configure(api_key=settings.GEMINI_API_KEY)
    # Create a Gemini model instance
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# System prompt to guide the chatbot's behavior
SYSTEM_PROMPT = """
You are Aaradhya, the professional AI assistant for Aaradhyadhrma, a leading software development and consulting company.

IMPORTANT GUIDELINES:

1. FOR GREETINGS (hello, hi, hey, etc.):
   ALWAYS respond with: "Hello! I'm Aaradhya, the AI assistant for Aaradhyadhrma. How can I help you with our services today?"

2. FOR QUESTIONS ABOUT OUR SERVICES:
   ALWAYS respond with the EXACT text:
   "Aaradhyadhrma specializes in:
   • Custom Software Development: Tailored solutions for business needs
   • AI/ML Integration: Cutting-edge artificial intelligence solutions
   • Full-stack Web & Mobile Development: End-to-end digital solutions
   • Technology Consultancy: Expert guidance on digital transformation
   
Which of our services are you interested in learning more about?"

3. FOR CONTACT REQUESTS (ANY mention of contact, connect, reach out, email, form, etc.):
   ALWAYS respond with EXACTLY: "__DISPLAY_CONTACT_FORM__"
   This special code will be replaced with an inline contact form in the chatbot.

4. FOR TEAM INFORMATION:
   "Our team at Aaradhyadhrma includes expert software developers, AI specialists, UX designers, and project managers with years of experience delivering high-quality digital solutions across various industries."

5. FOR ALL OFF-TOPIC QUESTIONS (programming help, personal advice, general tech, etc.):
   ALWAYS respond EXACTLY with: "I'm here specifically to help with information about Aaradhyadhrma's services and how to connect with our team. What would you like to know about our offerings?"

6. FOR AFFIRMATIVE RESPONSES (yes, sure, ok):
   Provide the services information from guideline #2.

7. FOR COMPANY INFORMATION:
   "Aaradhyadhrma is a technology company that combines innovative software solutions with ethical business practices. We specialize in creating custom software, AI integration, and digital transformation solutions for businesses of all sizes."

MAINTAIN CONVERSATION CONTEXT at all times. If you lose track of where you are in a conversation, refocus on learning about the user's needs related to our services.

NEVER provide coding help, technical explanations, or general advice unrelated to our company services.

REMEMBER: When someone asks to contact us, ONLY respond with: "__DISPLAY_CONTACT_FORM__"
"""

def get_conversation(session_id):
    """Get or create a conversation for the given session ID"""
    conversation, created = Conversation.objects.get_or_create(session_id=session_id)
    return conversation

def get_conversation_history(conversation):
    """Get the conversation history in the format expected by Gemini"""
    messages = conversation.messages.all().order_by('timestamp')
    history = []
    
    # ALWAYS start with the system prompt to enforce the behavior guidelines
    # This ensures the system prompt takes precedence over any conversation history
    history.append(SYSTEM_PROMPT)
    
    # Get the 10 most recent messages to keep context short and prevent LLM from building up knowledge
    # of off-topic conversations
    recent_messages = messages.filter(role__in=['user', 'assistant']).order_by('-timestamp')[:10]
    recent_messages = list(reversed(recent_messages))  # Reverse to get chronological order
    
    # Add filtered messages to history
    for message in recent_messages:
        # For Gemini API, we need to use the proper format without role/content keys
        if message.role == 'user':
            history.append(message.content)
        elif message.role == 'assistant':
            history.append(message.content)
    
    # Make sure we have the system prompt in the database too
    if not messages.filter(role='system').exists():
        system_message = Message(conversation=conversation, role='system', content=SYSTEM_PROMPT)
        system_message.save()
    
    return history

# Simple helper functions for contact form handling

def extract_contact_info(message):
    """Extract email addresses from user messages"""
    import re
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, message)
    
    if emails:
        return {'email': emails[0]}
    
    # If the message is very short and looks like a name
    words = message.strip().split()
    if len(words) <= 2 and not any(char.isdigit() for char in message):
        return {'name': message.strip()}
    
    return {}

def chatbot_response(user_message, session_id):
    """Generate a response from the chatbot using the simplified approach"""
    conversation = get_conversation(session_id)
    
    # Log user message
    logger.info(f"User ({session_id}): {user_message}")
    
    # Extract contact information if provided
    contact_info = extract_contact_info(user_message)
    if contact_info:
        # Update conversation with contact info directly
        if 'name' in contact_info and not conversation.name:
            conversation.name = contact_info['name']
            logger.info(f"Updated conversation {conversation.id} with name: {contact_info['name']}")
        
        if 'email' in contact_info and not conversation.email:
            conversation.email = contact_info['email']
            logger.info(f"Updated conversation {conversation.id} with email: {contact_info['email']}")
        
        conversation.save()
    
    # Save user message to database
    Message.objects.create(conversation=conversation, role='user', content=user_message)
    
    # Get conversation history with the improved system prompt
    history = get_conversation_history(conversation)
    
    # Check for keywords that indicate contact intent
    contact_keywords = ['contact', 'reach out', 'get in touch', 'connect', 'form', 'email', 'phone', 'support']
    is_contact_request = False
    
    # More robust contact detection
    message_lower = user_message.lower()
    for keyword in contact_keywords:
        if keyword in message_lower:
            is_contact_request = True
            break
    
    # If it's a clear contact request, skip the AI call and show the form directly
    if is_contact_request:
        response = "__DISPLAY_CONTACT_FORM__"
        logger.info(f"Contact intent detected, displaying form for session: {session_id}")
    else:
        # Generate response using Gemini
        if GEMINI_ENABLED:
            try:
                # Add the user's message to the history
                current_history = history.copy()
                current_history.append(user_message)
                
                # Log the conversation history being sent to Gemini
                logger.info(f"Sending to Gemini API ({session_id}): {current_history}")
                
                # Generate response
                gemini_response = model.generate_content(current_history)
                response = gemini_response.text
                
                # Log the raw Gemini response
                logger.info(f"Raw Gemini API response ({session_id}): {response}")
                
            except Exception as e:
                error_message = f"Gemini API error: {str(e)}"
                logger.error(f"{error_message} - Session ID: {session_id}")
                
                # Simple fallback response
                response = "I'm here specifically to help with information about Aaradhyadhrma's services and how to connect with our team. What would you like to know about our offerings?"
        else:
            # Fallback response when Gemini API is not available
            response = "I'm here specifically to help with information about Aaradhyadhrma's services and how to connect with our team. What would you like to know about our offerings?"
    
    # Save assistant response to database (original response with marker)
    Message.objects.create(conversation=conversation, role='assistant', content=response)
    
    # Log assistant response
    logger.info(f"Assistant ({session_id}): {response}")
    
    return response

def extract_contact_info(message):
    """Extract contact information from a message"""
    # Simple extraction logic - can be improved with NLP
    info = {}
    
    # Extract email
    import re
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, message)
    if emails:
        info['email'] = emails[0]
    
    # Extract phone (simple pattern)
    phone_pattern = r'\b\d{10}\b|\b\d{3}[-.]\d{3}[-.]\d{4}\b'
    phones = re.findall(phone_pattern, message)
    if phones:
        info['phone'] = phones[0]
    
    # Extract name (very basic approach)
    name_indicators = ['name is', 'I am', 'this is', 'call me']
    for indicator in name_indicators:
        if indicator in message.lower():
            parts = message.split(indicator, 1)
            if len(parts) > 1:
                potential_name = parts[1].strip().split('.')[0].split(',')[0].split('\n')[0]
                if len(potential_name.split()) <= 3 and len(potential_name) <= 50:
                    info['name'] = potential_name
                    break
    
    return info

def update_conversation_info(conversation, message):
    """Update conversation with extracted contact information"""
    info = extract_contact_info(message)
    updated = False
    
    if 'name' in info and not conversation.name:
        conversation.name = info['name']
        updated = True
    
    if 'email' in info and not conversation.email:
        conversation.email = info['email']
        updated = True
    
    if 'phone' in info and not conversation.phone:
        conversation.phone = info['phone']
        updated = True
    
    if updated:
        conversation.save()
    
    # Check if we have enough info to create a contact form
    if conversation.name and conversation.email and not conversation.is_contact_form_filled:
        # Look for a message that might be the inquiry content
        messages = conversation.messages.filter(role='user').order_by('-timestamp')[:5]
        for msg in messages:
            if len(msg.content) > 20 and not any(keyword in msg.content.lower() for keyword in ['my name is', 'my email is', 'my phone is']):
                # Create contact form
                ContactForm.objects.create(
                    name=conversation.name,
                    email=conversation.email,
                    phone=conversation.phone or '',
                    message=msg.content,
                    source='chatbot'
                )
                conversation.is_contact_form_filled = True
                conversation.save()
                return True
    
    return False

@csrf_exempt
def chat_api(request):
    """API endpoint for the chatbot"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            session_id = data.get('session_id', str(uuid.uuid4()))
            
            # Log the incoming API request
            logger.info(f"Chat API Request - Session ID: {session_id}, IP: {request.META.get('REMOTE_ADDR')}, User-Agent: {request.META.get('HTTP_USER_AGENT')}")
            
            # Get conversation
            conversation = get_conversation(session_id)
            
            # Check if this is a direct contact form submission
            if data.get('contact_form', False):
                # Process contact form data
                name = data.get('name', '')
                email = data.get('email', '')
                phone = data.get('phone', '')
                message = data.get('message', '')
                
                # Log the contact form submission
                logger.info(f"Contact form submitted - Session ID: {session_id}, Name: {name}, Email: {email}")
                
                # Update conversation with the provided info
                conversation.name = name
                conversation.email = email
                conversation.phone = phone
                conversation.is_contact_form_filled = True
                conversation.save()
                
                # Create a contact form entry
                from core.models import ContactForm
                ContactForm.objects.create(
                    name=name,
                    email=email,
                    phone=phone or '',
                    message=message,
                    source='chatbot'
                )
                
                # Save the message in the conversation history
                Message.objects.create(conversation=conversation, role='user', content=f"Contact form submission - Name: {name}, Email: {email}, Message: {message}")
                
                # Return success response
                response = "Thank you for submitting your contact information! Our team will get back to you soon. Is there anything else I can help you with?"
                
                # Save the assistant response
                Message.objects.create(conversation=conversation, role='assistant', content=response)
                
                return JsonResponse({
                    'response': response,
                    'session_id': session_id
                })
            
            # Normal message processing
            message = data.get('message', '')
            
            # Check for contact keywords before processing
            contact_keywords = ['contact', 'reach out', 'get in touch', 'connect', 'form', 'email', 'phone', 'support']
            is_contact_request = any(keyword in message.lower() for keyword in contact_keywords)
            
            if is_contact_request:
                # Directly return the special marker to show the contact form
                logger.info(f"Contact intent detected in API, displaying form for session: {session_id}")
                # Use a simple text marker that won't get modified
                return JsonResponse({
                    'response': "DISPLAY_CONTACT_FORM",
                    'session_id': session_id
                })
            
            # For non-contact messages, proceed normally
            # Update conversation with any contact info in the message
            form_submitted = update_conversation_info(conversation, message)
            
            # Generate response
            response = chatbot_response(message, session_id)
            
            # If a form was just submitted, append that information to the response
            if form_submitted:
                response += "\n\nThank you! I've submitted your contact information to our team. Someone will get back to you soon."
            
            return JsonResponse({
                'response': response,
                'session_id': session_id
            })
        except Exception as e:
            error_message = f"Chat API error: {str(e)}"
            logger.error(f"{error_message} - IP: {request.META.get('REMOTE_ADDR')}")
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

def chat_view(request):
    """Render the chat interface"""
    return render(request, 'chatbot/chat.html')
