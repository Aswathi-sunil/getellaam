const menuToggle = document.getElementById('menuToggle');
const navLinks = document.getElementById('navLinks');

if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
        navLinks.classList.toggle('active');
    });
}


// Counter animation
const counters = document.querySelectorAll('.counter');

const startCounter = (counter) => {
    const target = +counter.getAttribute('data-target');
    let current = 0;
    const increment = Math.max(1, Math.ceil(target / 80));

    const updateCounter = () => {
        current += increment;

        if (current < target) {
            counter.innerText = current;
            requestAnimationFrame(updateCounter);
        } else {
            counter.innerText = target + '+';
        }
    };

    updateCounter();
};

const counterObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            startCounter(entry.target);
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 });

counters.forEach(counter => {
    counterObserver.observe(counter);
});


// FAQ accordion
const faqItems = document.querySelectorAll('.faq-item');

faqItems.forEach(item => {
    const button = item.querySelector('.faq-question');

    button.addEventListener('click', () => {
        faqItems.forEach(otherItem => {
            if (otherItem !== item) {
                otherItem.classList.remove('active');
            }
        });

        item.classList.toggle('active');
    });
});


// Testimonial Swiper
document.addEventListener("DOMContentLoaded", function () {
    const testimonialSwiper = document.querySelector('.testimonialSwiper');

    if (testimonialSwiper) {
        new Swiper('.testimonialSwiper', {
            loop: true,
            spaceBetween: 25,
            autoplay: {
                delay: 2500,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            breakpoints: {
                0: { slidesPerView: 1 },
                768: { slidesPerView: 2 },
                992: { slidesPerView: 3 }
            }
        });
    }
});

const navbar = document.querySelector('.navbar');

window.addEventListener('scroll', () => {
    if (window.scrollY > 60) {
        navbar.classList.add('navbar-scrolled');
    } else {
        navbar.classList.remove('navbar-scrolled');
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const portfolioSwiper = document.querySelector('.portfolioSwiper');

    if (portfolioSwiper) {
        new Swiper('.portfolioSwiper', {
            loop: true,
            spaceBetween: 25,
            autoplay: {
                delay: 2800,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.portfolio-pagination',
                clickable: true,
            },
            breakpoints: {
                0: { slidesPerView: 1 },
                768: { slidesPerView: 2 },
                992: { slidesPerView: 3 }
            }
        });
    }
});

window.addEventListener('load', () => {
    const pageLoader = document.getElementById('pageLoader');

    if (pageLoader) {
        setTimeout(() => {
            pageLoader.classList.add('hide-loader');
        }, 500);
    }
});
const filterButtons = document.querySelectorAll('.filter-btn');
const filterItems = document.querySelectorAll('.filter-item');

filterButtons.forEach(button => {
    button.addEventListener('click', () => {
        const filterValue = button.getAttribute('data-filter');

        filterButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');

        filterItems.forEach(item => {
            const itemCategory = item.getAttribute('data-category');

            if (filterValue === 'all' || filterValue === itemCategory) {
                item.classList.remove('hide');
            } else {
                item.classList.add('hide');
            }
        });
    });
});
// Premium scroll reveal for elements that do not already use AOS
const motionTargets = document.querySelectorAll('.service-premium-card, .portfolio-tile, .timeline-card, .testimonial-card, .stat-premium, .logo-pill, .feature-list div');
motionTargets.forEach((el, index) => {
    el.classList.add('reveal-on-scroll');
    el.style.transitionDelay = `${Math.min(index % 4, 3) * 90}ms`;
});

const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('revealed');
            revealObserver.unobserve(entry.target);
        }
    });
}, { threshold: 0.14 });

document.querySelectorAll('.reveal-on-scroll').forEach(el => revealObserver.observe(el));

// Subtle 3D card tilt on desktop
const tiltCards = document.querySelectorAll('.service-premium-card, .portfolio-tile, .main-dashboard');
const canTilt = window.matchMedia('(min-width: 769px)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

if (canTilt) {
    tiltCards.forEach(card => {
        card.classList.add('tilt-active');
        card.addEventListener('mousemove', (e) => {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            const rotateY = ((x / rect.width) - 0.5) * 8;
            const rotateX = -((y / rect.height) - 0.5) * 8;
            card.style.transform = `translateY(-10px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
        card.addEventListener('mouseleave', () => {
            card.style.transform = '';
        });
    });
}

// Soft cursor glow for premium agency feel
const cursorGlow = document.getElementById('cursorGlow');
if (cursorGlow && canTilt) {
    document.addEventListener('mousemove', (e) => {
        cursorGlow.style.left = `${e.clientX}px`;
        cursorGlow.style.top = `${e.clientY}px`;
        cursorGlow.style.opacity = '1';
    });
    document.addEventListener('mouseleave', () => {
        cursorGlow.style.opacity = '0';
    });
}

// Magnetic button movement
const magneticButtons = document.querySelectorAll('.btn');
if (canTilt) {
    magneticButtons.forEach(btn => {
        btn.addEventListener('mousemove', (e) => {
            const rect = btn.getBoundingClientRect();
            const x = e.clientX - rect.left - rect.width / 2;
            const y = e.clientY - rect.top - rect.height / 2;
            btn.style.transform = `translate(${x * 0.08}px, ${y * 0.12}px)`;
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });
}

// Global premium 3D reveal + tilt for all public pages
(function () {
    const canMotion = window.matchMedia('(min-width: 769px)').matches && !window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    const revealItems = document.querySelectorAll('.reveal-3d, .depth-card, .depth-panel, .neo-service-card, .neo-portfolio-card, .job-card, .mission-card, .neo-feature-card');
    revealItems.forEach((el, index) => {
        el.classList.add('reveal-3d');
        el.style.transitionDelay = `${Math.min(index % 5, 4) * 75}ms`;
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.13 });

    document.querySelectorAll('.reveal-3d').forEach(el => observer.observe(el));

    if (!canMotion) return;

    const tiltItems = document.querySelectorAll('.depth-card, .depth-panel, .neo-visual-card, .neo-service-card, .neo-portfolio-card');
    tiltItems.forEach(card => {
        card.classList.add('tilt-active');
        card.addEventListener('mousemove', (event) => {
            const rect = card.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            const rotateY = ((x / rect.width) - .5) * 10;
            const rotateX = -((y / rect.height) - .5) * 10;
            card.style.transform = `translateY(-12px) rotateX(${rotateX}deg) rotateY(${rotateY}deg)`;
        });
        card.addEventListener('mouseleave', () => card.style.transform = '');
    });

    window.addEventListener('scroll', () => {
        const y = window.scrollY;
        document.querySelectorAll('.scene-orb, .hero-orb').forEach((orb, index) => {
            orb.style.transform = `translate3d(0, ${y * (0.035 + index * 0.015)}px, 0)`;
        });
    }, { passive: true });
})();
