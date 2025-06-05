"""
Context processor for allauth account pages
"""

def account_page_titles(request):
    """
    Add page titles for account templates to prevent VariableDoesNotExist errors
    """
    # Get the URL path
    path = request.path.strip('/')
    
    # Default title
    title = "Account - Aaradhyadhrma"
    
    # Set specific titles based on URL path
    if 'login' in path:
        title = "Sign In - Aaradhyadhrma"
    elif 'signup' in path:
        title = "Sign Up - Aaradhyadhrma"
    elif 'password/reset' in path:
        title = "Reset Password - Aaradhyadhrma"
    elif 'password/change' in path:
        title = "Change Password - Aaradhyadhrma"
    elif 'email' in path:
        title = "Manage Email - Aaradhyadhrma"
    elif 'logout' in path:
        title = "Sign Out - Aaradhyadhrma"
    
    return {
        'page_title': title,
        'og_title': title,
        'meta_description': "Account management pages for Aaradhyadhrma - Ancient Wisdom, Modern Solution",
        'og_description': "Account management pages for Aaradhyadhrma - Ancient Wisdom, Modern Solution",
    }
