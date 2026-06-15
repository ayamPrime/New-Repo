// El Vanta — Nav drawer toggle

document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-toggle');
    const navDrawer = document.querySelector('.nav-drawer');
    const navOverlay = document.querySelector('.nav-overlay');

    function closeNav() {
        navDrawer.classList.remove('open');
        navOverlay.classList.remove('open');
        navToggle.setAttribute('aria-expanded', 'false');
    }

    function toggleNav() {
        const isOpen = navDrawer.classList.toggle('open');
        navOverlay.classList.toggle('open');
        navToggle.setAttribute('aria-expanded', isOpen);
    }

    navToggle.addEventListener('click', toggleNav);
    navOverlay.addEventListener('click', closeNav);

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeNav();
    });
});