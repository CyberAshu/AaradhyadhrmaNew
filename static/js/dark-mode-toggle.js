/**
 * Dark Mode Toggle JavaScript for Aaradhyadhrma Website
 */

document.addEventListener('DOMContentLoaded', function() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const mobileDarkModeToggle = document.getElementById('mobileDarkMode');
    const html = document.documentElement;
    
    // Check for saved theme preference or use OS preference
    const savedTheme = localStorage.getItem('aaradhyadhrma-theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    // Set initial theme
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
        enableDarkMode();
    } else {
        disableDarkMode();
    }
    
    // Dark mode toggle click handler
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            if (html.classList.contains('dark-mode')) {
                disableDarkMode();
            } else {
                enableDarkMode();
            }
        });
    }
    
    // Function to enable dark mode
    function enableDarkMode() {
        html.classList.add('dark-mode');
        localStorage.setItem('aaradhyadhrma-theme', 'dark');
        
        // Update desktop toggle
        if (darkModeToggle) {
            darkModeToggle.setAttribute('aria-label', 'Switch to light mode');
            darkModeToggle.title = 'Switch to light mode';
        }
        
        // Update mobile toggle
        if (mobileDarkModeToggle) {
            mobileDarkModeToggle.checked = true;
        }
        
        // Update meta theme-color for mobile browsers
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', '#121825');
        }
        
        // Dispatch event for other scripts that might need to know about theme change
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: 'dark' } }));
    }
    
    // Function to disable dark mode
    function disableDarkMode() {
        html.classList.remove('dark-mode');
        localStorage.setItem('aaradhyadhrma-theme', 'light');
        
        // Update desktop toggle
        if (darkModeToggle) {
            darkModeToggle.setAttribute('aria-label', 'Switch to dark mode');
            darkModeToggle.title = 'Switch to dark mode';
        }
        
        // Update mobile toggle
        if (mobileDarkModeToggle) {
            mobileDarkModeToggle.checked = false;
        }
        
        // Update meta theme-color for mobile browsers
        const metaThemeColor = document.querySelector('meta[name="theme-color"]');
        if (metaThemeColor) {
            metaThemeColor.setAttribute('content', '#ffffff');
        }
        
        // Dispatch event for other scripts that might need to know about theme change
        document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: 'light' } }));
    }
    
    // Listen for OS theme preference changes
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        const savedTheme = localStorage.getItem('aaradhyadhrma-theme');
        if (!savedTheme) {
            if (e.matches) {
                enableDarkMode();
            } else {
                disableDarkMode();
            }
        }
    });
});
