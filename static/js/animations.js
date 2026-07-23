/* Site-wide animations, scroll reveals, and micro-interactions */

function prefersReducedMotion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

function revealOnScroll() {
    const simpleElements = document.querySelectorAll('[data-reveal]:not([data-reveal="stagger"])');
    const staggerContainers = document.querySelectorAll('[data-reveal="stagger"]');

    if ((!simpleElements.length && !staggerContainers.length) || prefersReducedMotion()) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (!entry.isIntersecting) return;

            const target = entry.target;

            if (target.matches('[data-reveal="stagger"]')) {
                target.classList.add('is-visible');
                const children = target.querySelectorAll('[data-reveal-child]');
                children.forEach((child, index) => {
                    setTimeout(() => child.classList.add('is-visible'), 60 * index);
                });
            } else {
                target.classList.add('is-visible');
            }

            observer.unobserve(target);
        });
    }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

    simpleElements.forEach((el) => observer.observe(el));
    staggerContainers.forEach((el) => observer.observe(el));
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

function initPageTransitions() {
    if (prefersReducedMotion()) return;
    const loader = document.querySelector('[data-page-loader]');
    if (!loader) return;

    document.querySelectorAll('a[href]:not([target]):not([href^="#"]):not([href^="mailto:"]):not([href^="tel:"])').forEach((link) => {
        const url = link.getAttribute('href');
        if (!url || url.startsWith('http') || url.startsWith('//')) return;

        link.addEventListener('click', (e) => {
            if (e.ctrlKey || e.metaKey || e.shiftKey || e.button !== 0) return;
            e.preventDefault();
            loader.classList.remove('is-loaded');
            loader.classList.add('is-loading');
            document.body.classList.add('page-is-exiting');
            setTimeout(() => {
                window.location.href = url;
            }, 220);
        });
    });
}

function initButtonRipple() {
    if (prefersReducedMotion()) return;
    document.querySelectorAll('button, .btn, .btn-browse, .btn-submit, .btn-enquire, .btn-inspect, .btn-pay, .back-button, .listing-link, .search-box button, .form-submit, .cta-button').forEach((btn) => {
        btn.addEventListener('click', function (e) {
            const rect = this.getBoundingClientRect();
            const ripple = document.createElement('span');
            ripple.className = 'btn-ripple';
            ripple.style.left = `${e.clientX - rect.left}px`;
            ripple.style.top = `${e.clientY - rect.top}px`;
            this.style.position = 'relative';
            this.style.overflow = 'hidden';
            this.appendChild(ripple);
            setTimeout(() => ripple.remove(), 600);
        });
    });
}

function initCardHover() {
    if (prefersReducedMotion()) return;
    document.querySelectorAll('.listing-card, .detail-panel, .summary-card, .form-section, .profile-card, .empty-listings').forEach((card) => {
        card.addEventListener('mouseenter', () => card.classList.add('is-hover'));
        card.addEventListener('mouseleave', () => card.classList.remove('is-hover'));
    });
}

function initIconEntrance() {
    if (prefersReducedMotion()) return;
    document.querySelectorAll('[data-icon-pop]').forEach((icon) => {
        icon.classList.add('icon-pop');
    });
}

function initImageSkeletons() {
    if (prefersReducedMotion()) return;
    document.querySelectorAll('img').forEach((img) => {
        if (img.complete) return;
        img.classList.add('img-skeleton');
        img.addEventListener('load', () => {
            img.classList.remove('img-skeleton');
            img.classList.add('img-loaded');
        }, { once: true });
        img.addEventListener('error', () => {
            img.classList.remove('img-skeleton');
        }, { once: true });
    });
}

document.addEventListener('DOMContentLoaded', () => {
    revealOnScroll();
    animateStepTransition();
    animateStepDone();
    initPageLoader();
    initPageTransitions();
    initButtonRipple();
    initCardHover();
    initIconEntrance();
    initImageSkeletons();
});
