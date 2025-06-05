// Chatbot JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatMessages = document.getElementById('chat-messages');
    
    // Session ID for conversation tracking (stored in localStorage)
    let sessionId = localStorage.getItem('chatSessionId');
    if (!sessionId) {
        sessionId = generateSessionId();
        localStorage.setItem('chatSessionId', sessionId);
    }
    
    // Add event listener for form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        sendUserMessage();
    });
    
    // Add event listener for Enter key
    userInput.addEventListener('keydown', function(e) {
        // Send message on Enter without Shift key
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendUserMessage();
        }
    });
    
    // Function to handle sending user messages
    function sendUserMessage() {
        const message = userInput.value.trim();
        if (message) {
            // Add user message to chat
            addMessage('user', message);
            
            // Clear input
            userInput.value = '';
            
            // Show typing indicator
            showTypingIndicator();
            
            // Send message to server
            sendMessage(message);
        }
    }
    
    // Function to create and display a contact form in the chat
    function showContactForm() {
        const formDiv = document.createElement('div');
        formDiv.classList.add('message', 'assistant', 'contact-form-container');
        
        const formContent = `
            <div class="message-avatar">
                <img src="/static/images/logo-icon.png" alt="Assistant">
            </div>
            <div class="message-content contact-form">
                <h4>Direct Contact Form</h4>
                <p>This form will submit your information directly to the Aaradhyadhrma team. No need for email - just fill out the details below:</p>
                <form id="chat-contact-form">
                    <div class="form-group">
                        <input type="text" id="contact-name" placeholder="Your Name" required>
                    </div>
                    <div class="form-group">
                        <input type="email" id="contact-email" placeholder="Your Email" required>
                    </div>
                    <div class="form-group">
                        <input type="tel" id="contact-phone" placeholder="Your Phone (optional)">
                    </div>
                    <div class="form-group">
                        <textarea id="contact-message" placeholder="Describe what you need help with" required></textarea>
                    </div>
                    <p class="form-note">Your information will be sent directly to our team, and someone will contact you soon.</p>
                    <button type="submit" class="btn-submit">Submit Contact Request</button>
                </form>
            </div>
        `;
        
        formDiv.innerHTML = formContent;
        chatMessages.appendChild(formDiv);
        formDiv.classList.add('show');
        
        // Add event listener to the form
        const contactForm = document.getElementById('chat-contact-form');
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitContactForm();
        });
        
        scrollToBottom();
    }
    
    // Function to submit the contact form
    function submitContactForm() {
        const name = document.getElementById('contact-name').value.trim();
        const email = document.getElementById('contact-email').value.trim();
        const phone = document.getElementById('contact-phone').value.trim();
        const message = document.getElementById('contact-message').value.trim();
        
        // Remove the form
        const formContainer = document.querySelector('.contact-form-container');
        if (formContainer) {
            formContainer.remove();
        }
        
        // Show processing message
        addMessage('assistant', 'Processing your submission...');
        showTypingIndicator();
        
        // Prepare the data
        const contactData = {
            session_id: sessionId,
            contact_form: true,
            name: name,
            email: email,
            phone: phone,
            message: message
        };
        
        // Send to server
        fetch('/chatbot/api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(contactData)
        })
        .then(response => response.json())
        .then(data => {
            removeTypingIndicator();
            addMessage('assistant', data.response);
        })
        .catch(error => {
            removeTypingIndicator();
            addMessage('assistant', 'Sorry, there was an error submitting your contact form. Please try again later.');
            console.error('Error:', error);
        });
    }
    
    // Function to add a message to the chat
    function addMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', role);
        
        const currentTime = new Date();
        const timeString = currentTime.getHours() + ':' + 
                          (currentTime.getMinutes() < 10 ? '0' : '') + currentTime.getMinutes();
        
        // Add avatar for assistant messages
        let avatarHtml = '';
        if (role === 'assistant') {
            avatarHtml = `<div class="message-avatar">
                <img src="/static/images/logo.svg" alt="Aaradhya AI">
            </div>`;
        }
        
        messageDiv.innerHTML = `
            ${avatarHtml}
            <div class="message-bubble">
                <div class="message-content">
                    <p>${formatMessage(content)}</p>
                </div>
                <div class="message-time">${timeString}</div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        
        // Add animation class after a small delay to trigger animation
        setTimeout(() => {
            messageDiv.classList.add('show');
        }, 10);
        
        // Scroll to bottom
        scrollToBottom();
    }
    
    // Function to format message with markdown-like syntax
    function formatMessage(content) {
        // Replace URLs with links
        content = content.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
        );
        
        // Replace newlines with <br>
        content = content.replace(/\n/g, '<br>');
        
        // Bold text between **
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Italic text between *
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        return content;
    }
    
    // Function to show typing indicator
    function showTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'assistant', 'typing-message');
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <img src="/static/images/logo.svg" alt="Aaradhya AI">
            </div>
            <div class="message-bubble">
                <div class="message-content typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(typingDiv);
        
        // Add show class after a small delay to trigger animation
        setTimeout(() => {
            typingDiv.classList.add('show');
        }, 10);
        
        scrollToBottom();
        
        return typingDiv;
    }
    
    // Function to remove typing indicator
    function removeTypingIndicator() {
        const typingMessage = document.querySelector('.typing-message');
        if (typingMessage) {
            // Fade out animation
            typingMessage.classList.remove('show');
            
            // Remove after animation completes
            setTimeout(() => {
                typingMessage.remove();
            }, 300);
        }
    }
    
    // Function to scroll chat to bottom
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to send message to server
    function sendMessage(message) {
        // Check if the message is asking for contact form
        if ((message.toLowerCase().includes('contact') && 
             (message.toLowerCase().includes('form') || message.toLowerCase().includes('submit') || 
              message.toLowerCase().includes('get in touch') || message.toLowerCase().includes('reach out'))) ||
            (message.toLowerCase().includes('through you')) ||
            (message.toLowerCase().includes('send through') || message.toLowerCase().includes('send via')) ||
            (message.toLowerCase().includes('not through mail') || message.toLowerCase().includes('not via email')) ||
            (message.toLowerCase().includes('fill') && message.toLowerCase().includes('form'))) {
            
            // Store contact intent in localStorage
            localStorage.setItem('contactIntent', 'true');
            localStorage.setItem('contactIntentTime', Date.now());
            
            // Show contact form after a short delay
            setTimeout(() => {
                removeTypingIndicator();
                showContactForm();
            }, 1000);
            return;
        }
        
        // Check if user has previously expressed contact intent and is now responding to the prompt
        const contactIntent = localStorage.getItem('contactIntent');
        const contactIntentTime = localStorage.getItem('contactIntentTime');
        const oneHourInMs = 60 * 60 * 1000;
        
        // If the user had contact intent within the last hour and now types 'contact form'
        if (contactIntent === 'true' && 
            contactIntentTime && 
            (Date.now() - parseInt(contactIntentTime)) < oneHourInMs && 
            message.toLowerCase() === 'contact form') {
            
            // Show contact form after a short delay
            setTimeout(() => {
                removeTypingIndicator();
                showContactForm();
            }, 1000);
            return;
        }
        
        // Add a small delay to make the typing indicator visible for at least a moment
        // This makes the chat feel more natural
        const minTypingTime = 1000; // 1 second minimum typing time
        const typingStartTime = Date.now();
        
        fetch('/chatbot/api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Calculate how long the typing indicator has been shown
            const typingDuration = Date.now() - typingStartTime;
            const remainingDelay = Math.max(0, minTypingTime - typingDuration);
            
            // Add a delay if needed to ensure minimum typing time
            setTimeout(() => {
                // Remove typing indicator
                removeTypingIndicator();
                
                // Check if the response is the special contact form marker
                if (data.response === "DISPLAY_CONTACT_FORM") {
                    showContactForm();
                } else {
                    // Add regular response to chat
                    addMessage('assistant', data.response);
                }
                
                // Update session ID if it changed
                if (data.session_id && data.session_id !== sessionId) {
                    sessionId = data.session_id;
                    localStorage.setItem('chatSessionId', sessionId);
                }
            }, remainingDelay);
        })
        .catch(error => {
            console.error('Error:', error);
            
            // Remove typing indicator
            removeTypingIndicator();
            
            // Add error message
            addMessage('assistant', 'Sorry, I encountered an error. Please try again later.');
        });
    }
    
    // Function to generate a session ID
    function generateSessionId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
});

// Floating Chat Widget
document.addEventListener('DOMContentLoaded', function() {
    // Create the chat widget button
    const chatWidgetButton = document.createElement('div');
    chatWidgetButton.classList.add('chat-widget-button');
    chatWidgetButton.innerHTML = '<i class="fas fa-comments"></i>';
    document.body.appendChild(chatWidgetButton);
    
    // Create the chat widget container
    const chatWidgetContainer = document.createElement('div');
    chatWidgetContainer.classList.add('chat-widget-container');
    document.body.appendChild(chatWidgetContainer);
    
    // Chat widget HTML
    chatWidgetContainer.innerHTML = `
        <div class="chat-container">
            <div class="chat-header">
                <div class="chat-header-title">
                    <img src="/static/images/logo.svg" alt="Aaradhyadhrma Logo" class="chat-logo">
                    <div>
                        <h3>Aaradhya AI Assistant</h3>
                        <span class="status-indicator">Online</span>
                    </div>
                </div>
                <button class="chat-close-button" aria-label="Close chat">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="chat-messages" id="widget-chat-messages">
                <div class="message assistant">
                    <div class="message-content">
                        <p>Hello! I'm Aaradhya, your AI assistant. How can I help you today?</p>
                    </div>
                    <div class="message-time">Just now</div>
                </div>
            </div>
            <div class="chat-input-container">
                <form id="widget-chat-form">
                    <div class="input-group">
                        <input type="text" id="widget-user-input" class="form-control" placeholder="Type your message here..." autocomplete="off">
                        <div class="input-group-append">
                            <button class="btn btn-primary" type="submit">
                                <i class="fas fa-paper-plane"></i>
                            </button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    `;
    
    // Toggle chat widget
    chatWidgetButton.addEventListener('click', function() {
        chatWidgetContainer.classList.toggle('active');
        
        // If opening the widget, focus the input
        if (chatWidgetContainer.classList.contains('active')) {
            document.getElementById('widget-user-input').focus();
            
            // Add click event to close button after widget is opened
            // This ensures the button exists in the DOM when we try to attach the event
            setTimeout(function() {
                const closeButton = document.querySelector('.chat-close-button');
                if (closeButton) {
                    // Remove any existing listeners to avoid duplicates
                    closeButton.replaceWith(closeButton.cloneNode(true));
                    
                    // Add new listener
                    document.querySelector('.chat-close-button').addEventListener('click', function(e) {
                        e.stopPropagation(); // Prevent event bubbling
                        chatWidgetContainer.classList.remove('active');
                    });
                }
            }, 100);
        }
    });
    
    // Elements for the widget
    const widgetChatForm = document.getElementById('widget-chat-form');
    const widgetUserInput = document.getElementById('widget-user-input');
    const widgetChatMessages = document.getElementById('widget-chat-messages');
    
    // Session ID for conversation tracking (stored in localStorage)
    let sessionId = localStorage.getItem('chatSessionId');
    if (!sessionId) {
        sessionId = generateSessionId();
        localStorage.setItem('chatSessionId', sessionId);
    }
    
    // Add event listener for form submission
    widgetChatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        sendWidgetUserMessage();
    });
    
    // Add event listener for Enter key
    widgetUserInput.addEventListener('keydown', function(e) {
        // Send message on Enter without Shift key
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendWidgetUserMessage();
        }
    });
    
    // Function to handle sending user messages in widget
    function sendWidgetUserMessage() {
        const message = widgetUserInput.value.trim();
        if (message) {
            // Add user message to chat
            addWidgetMessage('user', message);
            
            // Clear input
            widgetUserInput.value = '';
            
            // Show typing indicator
            showWidgetTypingIndicator();
            
            // Send message to server
            sendWidgetMessage(message);
        }
    }
    
    // Function to add a message to the widget chat
    function addWidgetMessage(role, content) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', role);
        
        const currentTime = new Date();
        const timeString = currentTime.getHours() + ':' + 
                          (currentTime.getMinutes() < 10 ? '0' : '') + currentTime.getMinutes();
        
        // Add avatar for assistant messages
        let avatarHtml = '';
        if (role === 'assistant') {
            avatarHtml = `<div class="message-avatar">
                <img src="/static/images/logo.svg" alt="Aaradhya AI">
            </div>`;
        }
        
        messageDiv.innerHTML = `
            ${avatarHtml}
            <div class="message-bubble">
                <div class="message-content">
                    <p>${formatWidgetMessage(content)}</p>
                </div>
                <div class="message-time">${timeString}</div>
            </div>
        `;
        
        widgetChatMessages.appendChild(messageDiv);
        
        // Add animation class after a small delay to trigger animation
        setTimeout(() => {
            messageDiv.classList.add('show');
        }, 10);
        
        // Scroll to bottom
        scrollWidgetToBottom();
    }
    
    // Function to format message with markdown-like syntax
    function formatWidgetMessage(content) {
        // Replace URLs with links
        content = content.replace(
            /(https?:\/\/[^\s]+)/g, 
            '<a href="$1" target="_blank" rel="noopener noreferrer">$1</a>'
        );
        
        // Replace newlines with <br>
        content = content.replace(/\n/g, '<br>');
        
        // Bold text between **
        content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Italic text between *
        content = content.replace(/\*(.*?)\*/g, '<em>$1</em>');
        
        return content;
    }
    
    // Function to show typing indicator in widget
    function showWidgetTypingIndicator() {
        const typingDiv = document.createElement('div');
        typingDiv.classList.add('message', 'assistant', 'widget-typing-message');
        
        typingDiv.innerHTML = `
            <div class="message-avatar">
                <img src="/static/images/logo.svg" alt="Aaradhya AI">
            </div>
            <div class="message-bubble">
                <div class="message-content typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                </div>
            </div>
        `;
        
        widgetChatMessages.appendChild(typingDiv);
        
        // Add show class after a small delay to trigger animation
        setTimeout(() => {
            typingDiv.classList.add('show');
        }, 10);
        
        scrollWidgetToBottom();
        
        return typingDiv;
    }
    
    // Function to remove typing indicator from widget
    function removeWidgetTypingIndicator() {
        const typingMessage = document.querySelector('.widget-typing-message');
        if (typingMessage) {
            // Fade out animation
            typingMessage.classList.remove('show');
            
            // Remove after animation completes
            setTimeout(() => {
                typingMessage.remove();
            }, 300);
        }
    }
    
    // Function to scroll widget chat to bottom
    function scrollWidgetToBottom() {
        widgetChatMessages.scrollTop = widgetChatMessages.scrollHeight;
    }
    
    // Function to create and display a contact form in the widget chat
    function showWidgetContactForm() {
        const formDiv = document.createElement('div');
        formDiv.classList.add('message', 'assistant', 'contact-form-container');
        
        const formContent = `
            <div class="message-avatar">
                <img src="/static/images/logo-icon.png" alt="Assistant">
            </div>
            <div class="message-content contact-form">
                <h4>Direct Contact Form</h4>
                <p>This form will submit your information directly to the Aaradhyadhrma team. No need for email - just fill out the details below:</p>
                <form id="widget-contact-form">
                    <div class="form-group">
                        <input type="text" id="widget-contact-name" placeholder="Your Name" required>
                    </div>
                    <div class="form-group">
                        <input type="email" id="widget-contact-email" placeholder="Your Email" required>
                    </div>
                    <div class="form-group">
                        <input type="tel" id="widget-contact-phone" placeholder="Your Phone (optional)">
                    </div>
                    <div class="form-group">
                        <textarea id="widget-contact-message" placeholder="Describe what you need help with" required></textarea>
                    </div>
                    <p class="form-note">Your information will be sent directly to our team, and someone will contact you soon.</p>
                    <button type="submit" class="btn-submit">Submit Contact Request</button>
                </form>
            </div>
        `;
        
        formDiv.innerHTML = formContent;
        widgetChatMessages.appendChild(formDiv);
        formDiv.classList.add('show');
        
        // Add event listener to the form
        const contactForm = document.getElementById('widget-contact-form');
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitWidgetContactForm();
        });
        
        scrollWidgetToBottom();
    }

    // Function to submit the contact form from widget
    function submitWidgetContactForm() {
        const name = document.getElementById('widget-contact-name').value.trim();
        const email = document.getElementById('widget-contact-email').value.trim();
        const phone = document.getElementById('widget-contact-phone').value.trim();
        const message = document.getElementById('widget-contact-message').value.trim();
        
        // Remove the form
        const formContainer = document.querySelector('.contact-form-container');
        if (formContainer) {
            formContainer.remove();
        }
        
        // Show processing message
        addWidgetMessage('assistant', 'Processing your submission...');
        showWidgetTypingIndicator();
        
        // Prepare the data
        const contactData = {
            session_id: sessionId,
            contact_form: true,
            name: name,
            email: email,
            phone: phone,
            message: message
        };
        
        // Send to server
        fetch('/chatbot/api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(contactData)
        })
        .then(response => response.json())
        .then(data => {
            removeWidgetTypingIndicator();
            addWidgetMessage('assistant', data.response);
        })
        .catch(error => {
            removeWidgetTypingIndicator();
            addWidgetMessage('assistant', 'Sorry, there was an error submitting your contact form. Please try again later.');
            console.error('Error:', error);
        });
    }

    // Function to send message to server from widget
    function sendWidgetMessage(message) {
        // Check if the message is asking for contact form
        if ((message.toLowerCase().includes('contact') && 
             (message.toLowerCase().includes('form') || message.toLowerCase().includes('submit') || 
              message.toLowerCase().includes('get in touch') || message.toLowerCase().includes('reach out'))) ||
            (message.toLowerCase().includes('through you')) ||
            (message.toLowerCase().includes('send through') || message.toLowerCase().includes('send via')) ||
            (message.toLowerCase().includes('not through mail') || message.toLowerCase().includes('not via email')) ||
            (message.toLowerCase().includes('fill') && message.toLowerCase().includes('form'))) {
            
            // Store contact intent in localStorage
            localStorage.setItem('contactIntent', 'true');
            localStorage.setItem('contactIntentTime', Date.now());
            
            // Show contact form after a short delay
            setTimeout(() => {
                removeWidgetTypingIndicator();
                showWidgetContactForm();
            }, 1000);
            return;
        }
        
        // Check if user has previously expressed contact intent and is now responding to the prompt
        const contactIntent = localStorage.getItem('contactIntent');
        const contactIntentTime = localStorage.getItem('contactIntentTime');
        const oneHourInMs = 60 * 60 * 1000;
        
        // If the user had contact intent within the last hour and now types 'contact form'
        if (contactIntent === 'true' && 
            contactIntentTime && 
            (Date.now() - parseInt(contactIntentTime)) < oneHourInMs && 
            message.toLowerCase() === 'contact form') {
            
            // Show contact form after a short delay
            setTimeout(() => {
                removeWidgetTypingIndicator();
                showWidgetContactForm();
            }, 1000);
            return;
        }
        
        // Add a small delay to make the typing indicator visible for at least a moment
        // This makes the chat feel more natural
        const minTypingTime = 1000; // 1 second minimum typing time
        const typingStartTime = Date.now();
        
        fetch('/chatbot/api/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Calculate how long the typing indicator has been shown
            const typingDuration = Date.now() - typingStartTime;
            const remainingDelay = Math.max(0, minTypingTime - typingDuration);
            
            // Add a delay if needed to ensure minimum typing time
            setTimeout(() => {
                // Remove typing indicator
                removeWidgetTypingIndicator();
                
                // Check if the response is the special contact form marker
                if (data.response === "DISPLAY_CONTACT_FORM") {
                    showWidgetContactForm();
                } else {
                    // Add regular response to widget chat
                    addWidgetMessage('assistant', data.response);
                }
                
                // Update session ID if it changed
                if (data.session_id && data.session_id !== sessionId) {
                    sessionId = data.session_id;
                    localStorage.setItem('chatSessionId', sessionId);
                }
            }, remainingDelay);
        })
        .catch(error => {
            console.error('Error:', error);
            
            // Remove typing indicator
            removeWidgetTypingIndicator();
            
            // Add error message
            addWidgetMessage('assistant', 'Sorry, I encountered an error. Please try again later.');
        });
    }
    
    // Function to generate a session ID
    function generateSessionId() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c === 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
});
