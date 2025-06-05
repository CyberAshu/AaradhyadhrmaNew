/**
 * Main JavaScript file for Aaradhyadhrma Website
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS animations
    AOS.init({
        duration: 800,
        easing: 'ease-in-out',
        once: true,
        mirror: false
    });
    
    // Add active class to nav links based on current page
    const currentLocation = window.location.pathname;
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    
    navLinks.forEach(link => {
        const linkPath = link.getAttribute('href');
        if (linkPath && currentLocation.includes(linkPath) && linkPath !== '/') {
            link.classList.add('active');
        } else if (linkPath === '/' && currentLocation === '/') {
            link.classList.add('active');
        }
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Back to top button
    const backToTopButton = document.getElementById('back-to-top');
    if (backToTopButton) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopButton.classList.add('show');
            } else {
                backToTopButton.classList.remove('show');
            }
        });
        
        backToTopButton.addEventListener('click', (e) => {
            e.preventDefault();
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }
    
    // Newsletter form submission (placeholder)
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            const emailInput = this.querySelector('input[type="email"]');
            if (emailInput && emailInput.value) {
                // Here you would normally send this to your backend
                alert('Thank you for subscribing to our newsletter!');
                emailInput.value = '';
            }
        });
    });
    
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-dismiss alerts
    const autoAlerts = document.querySelectorAll('.alert-dismissible.auto-dismiss');
    autoAlerts.forEach(alert => {
        setTimeout(() => {
            const closeButton = alert.querySelector('.btn-close');
            if (closeButton) {
                closeButton.click();
            }
        }, 5000);
    });
    
    // Handle video testimonials
    const clientVideos = document.querySelectorAll('.client-video');
    clientVideos.forEach(video => {
        // Make sure video loads correctly
        video.addEventListener('loadedmetadata', function() {
            console.log('Video metadata loaded:', this.src);
        });
        
        // Log errors if video fails to load
        video.addEventListener('error', function(e) {
            console.error('Error loading video:', this.src, e);
        });
        
        // Add poster click to play functionality
        if (video.hasAttribute('poster')) {
            const videoContainer = video.closest('.video-container');
            if (videoContainer) {
                // Add play overlay if not already present
                if (!videoContainer.querySelector('.play-overlay')) {
                    const playOverlay = document.createElement('div');
                    playOverlay.className = 'play-overlay';
                    playOverlay.innerHTML = '<i class="fas fa-play"></i>';
                    videoContainer.appendChild(playOverlay);
                    
                    // Play video when overlay is clicked
                    playOverlay.addEventListener('click', function() {
                        if (video.paused) {
                            video.play();
                            this.style.display = 'none';
                        }
                    });
                    
                    // Show overlay when video ends
                    video.addEventListener('ended', function() {
                        playOverlay.style.display = 'flex';
                    });
                    
                    // Add click event to the video to toggle play/pause
                    video.addEventListener('click', function() {
                        if (this.paused) {
                            this.play();
                            if (playOverlay) playOverlay.style.display = 'none';
                        } else {
                            this.pause();
                            if (playOverlay) playOverlay.style.display = 'flex';
                        }
                    });
                }
            }
        }
    });

    
    // File input custom display
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const fileName = this.files[0]?.name;
            const label = this.nextElementSibling;
            if (label && label.classList.contains('form-text')) {
                if (fileName) {
                    label.textContent = `Selected file: ${fileName}`;
                } else {
                    label.textContent = 'Upload your resume (PDF, DOC, or DOCX format, max 5MB)';
                }
            }
        });
    });
    
    // Close mobile menu when clicking outside
    document.addEventListener('click', function(event) {
        const navbar = document.getElementById('navbarNav');
        const navbarToggler = document.querySelector('.navbar-toggler');
        
        if (navbar.classList.contains('show') && !navbar.contains(event.target) && !navbarToggler.contains(event.target)) {
            navbar.classList.remove('show');
        }
    });
});
