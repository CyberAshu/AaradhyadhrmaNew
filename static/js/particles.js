/**
 * Hero Section Particles Animation
 * Creates an interactive particle background effect for the hero section
 */
document.addEventListener('DOMContentLoaded', function() {
    // Check if the hero particles container exists
    const particlesContainer = document.getElementById('hero-particles');
    if (!particlesContainer) return;
    
    // Particle settings
    const PARTICLE_COUNT = 50;
    const PARTICLE_SIZE_MIN = 1;
    const PARTICLE_SIZE_MAX = 3;
    const PARTICLE_SPEED_MIN = 0.1;
    const PARTICLE_SPEED_MAX = 0.3;
    const CONNECTION_DISTANCE = 150;
    const CONNECTION_WIDTH = 0.5;
    
    // Canvas setup
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    particlesContainer.appendChild(canvas);
    
    // Set canvas size to match container
    function resizeCanvas() {
        canvas.width = particlesContainer.offsetWidth;
        canvas.height = particlesContainer.offsetHeight;
    }
    
    // Listen for window resize
    window.addEventListener('resize', resizeCanvas);
    resizeCanvas();
    
    // Particle class
    class Particle {
        constructor() {
            this.x = Math.random() * canvas.width;
            this.y = Math.random() * canvas.height;
            this.size = PARTICLE_SIZE_MIN + Math.random() * (PARTICLE_SIZE_MAX - PARTICLE_SIZE_MIN);
            this.speedX = (Math.random() - 0.5) * (PARTICLE_SPEED_MAX - PARTICLE_SPEED_MIN);
            this.speedY = (Math.random() - 0.5) * (PARTICLE_SPEED_MAX - PARTICLE_SPEED_MIN);
            this.color = 'rgba(110, 143, 255, ';
            this.opacity = 0.1 + Math.random() * 0.4;
        }
        
        // Update particle position
        update() {
            this.x += this.speedX;
            this.y += this.speedY;
            
            // Bounce off edges
            if (this.x > canvas.width || this.x < 0) {
                this.speedX = -this.speedX;
            }
            
            if (this.y > canvas.height || this.y < 0) {
                this.speedY = -this.speedY;
            }
        }
        
        // Draw particle
        draw() {
            ctx.fillStyle = this.color + this.opacity + ')';
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
            ctx.fill();
        }
    }
    
    // Create particles
    const particles = [];
    for (let i = 0; i < PARTICLE_COUNT; i++) {
        particles.push(new Particle());
    }
    
    // Mouse interaction
    let mouse = {
        x: null,
        y: null,
        radius: 100
    };
    
    window.addEventListener('mousemove', function(event) {
        const rect = canvas.getBoundingClientRect();
        mouse.x = event.clientX - rect.left;
        mouse.y = event.clientY - rect.top;
    });
    
    // Animation loop
    function animate() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Update and draw particles
        for (let i = 0; i < particles.length; i++) {
            particles[i].update();
            particles[i].draw();
            
            // Connect particles
            for (let j = i; j < particles.length; j++) {
                const dx = particles[i].x - particles[j].x;
                const dy = particles[i].y - particles[j].y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < CONNECTION_DISTANCE) {
                    // Calculate opacity based on distance
                    const opacity = 1 - (distance / CONNECTION_DISTANCE);
                    
                    ctx.strokeStyle = `rgba(110, 143, 255, ${opacity * 0.2})`;
                    ctx.lineWidth = CONNECTION_WIDTH;
                    ctx.beginPath();
                    ctx.moveTo(particles[i].x, particles[i].y);
                    ctx.lineTo(particles[j].x, particles[j].y);
                    ctx.stroke();
                }
            }
            
            // Mouse interaction
            if (mouse.x !== null && mouse.y !== null) {
                const dx = particles[i].x - mouse.x;
                const dy = particles[i].y - mouse.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < mouse.radius) {
                    // Move particles away from mouse
                    const forceDirectionX = dx / distance;
                    const forceDirectionY = dy / distance;
                    const force = (mouse.radius - distance) / mouse.radius;
                    
                    particles[i].x += forceDirectionX * force * 2;
                    particles[i].y += forceDirectionY * force * 2;
                }
            }
        }
        
        requestAnimationFrame(animate);
    }
    
    animate();
});
