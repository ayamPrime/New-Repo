/* Site-wide animations and scroll reveals */

function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function revealOnScroll() {
    const elements = document.querySelectorAll('[data-reveal]');
    if (!elements.length || prefersReducedMotion()) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    elements.forEach((el) => observer.observe(el));
}

function animateStepTransition() {
    const forms = document.querySelectorAll('[data-signup-step]');
    if (!forms.length || prefersReducedMotion()) return;

    forms.forEach((form) => {
        form.classList.add('step-enter');
        requestAnimationFrame(() => {
            form.classList.add('step-enter-active');
        });
    });
}

function animateStepDone() {
    document.querySelectorAll('.step-dot.done').forEach((dot) => {
        dot.classList.add('step-complete');
    });
}

function initPageLoader() {
    if (prefersReducedMotion()) return;
    const loader = document.querySelector('[data-page-loader]');
    if (!loader) return;
    loader.classList.add('is-loading');
    window.addEventListener('load', () => {
        loader.classList.remove('is-loading');
        loader.classList.add('is-loaded');
    });
}

function initButtonRipple() {
    if (prefersReducedMotion()) return;
    document.querySelectorAll('button, .btn-browse, .btn-submit, .btn-enquire, .btn-inspect, .btn-pay, .back-button, .listing-link').forEach((btn) => {
        btn.addEventListener('click', function (e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            ripple.className = 'btn-ripple';
            ripple.style.left = `${e.clientX - rect.left}px`;
            ripple.style.top = `${e.clientY - rect.top}px`;
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

function initCardHover() {
    if (prefersReducedMotion()) return;
    document.querySelectorAll('.listing-card, .detail-panel, .summary-card, .form-section, .profile-card').forEach((card) => {
        card.addEventListener('mouseenter', () => card.classList.add('is-hover'));
        card.addEventListener('mouseleave', () => card.classList.remove('is-hover'));
    });
}

document.addEventListener('DOMContentLoaded', () => {
    revealOnScroll();
    animateStepTransition();
    animateStepDone();
    initPageLoader();
    initButtonRipple();
    initCardHover();
});
