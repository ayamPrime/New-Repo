(function () {
  var pre = document.getElementById('vcPre');
  var fill = document.getElementById('vcPreFill');
  if (!pre || !fill) return;

  fill.style.transition = 'width 1.45s cubic-bezier(.4,0,.2,1)';
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { fill.style.width = '100%'; });
  });

  setTimeout(function () {
    pre.style.transition = 'transform .8s cubic-bezier(.76,0,.24,1), opacity .35s ease';
    pre.style.transform = 'translateY(-100%)';
    pre.style.opacity = '0';
    setTimeout(function () {
      pre.style.display = 'none';
      startHero();
    }, 750);
  }, 1650);
})();

function startHero() {
  if (typeof gsap === 'undefined') { fallback(); return; }

  gsap.registerPlugin(ScrollTrigger);

  if (typeof Lenis !== 'undefined') {
    var lenis = new Lenis({ duration: 1.25, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); } });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (time) { lenis.raf(time * 1000); });
    gsap.ticker.lagSmoothing(0);
  }

  var tl = gsap.timeline({ defaults: { ease: 'power4.out' } });
  tl.to('#vcEye', { opacity: 1, y: 0, duration: .8 }, 0.1);
  tl.to('#vcW1', { y: '0%', duration: 1.15 }, 0.22);
  tl.to('#vcW2', { y: '0%', duration: 1.15 }, 0.38);
  tl.to('#vcW3', { y: '0%', duration: 1.15 }, 0.54);
  tl.to('#vcSub', { opacity: 1, duration: .9 }, 0.62);
  tl.to('#vcSearch', { opacity: 1, y: 0, duration: .9 }, 0.74);

  document.querySelectorAll('[data-reveal]').forEach(function (el) {
    var delay = parseFloat(el.dataset.delay || 0) / 1000;
    gsap.fromTo(el,
      { opacity: 0, y: 26 },
      {
        opacity: 1, y: 0, duration: .7, delay: delay, ease: 'power3.out',
        scrollTrigger: { trigger: el, start: 'top 88%', toggleActions: 'play none none none' }
      }
    );
  });

  gsap.fromTo('.vc-how__step',
    { opacity: 0, y: 36 },
    { opacity: 1, y: 0, stagger: .14, duration: .75, ease: 'power3.out',
      scrollTrigger: { trigger: '.vc-how__grid', start: 'top 82%' } }
  );

  gsap.fromTo('.vc-trust-bar__item',
    { opacity: 0, y: 16 },
    { opacity: 1, y: 0, stagger: .1, duration: .6, ease: 'power3.out',
      scrollTrigger: { trigger: '.vc-trust-bar', start: 'top 90%' } }
  );

  gsap.to('.vc-field__img', {
    yPercent: -14,
    ease: 'none',
    scrollTrigger: { trigger: '.vc-field', scrub: true }
  });

  gsap.fromTo('.vc-field__title',
    { clipPath: 'inset(0 100% 0 0)' },
    { clipPath: 'inset(0 0% 0 0)', duration: 1.1, ease: 'power3.inOut',
      scrollTrigger: { trigger: '.vc-field__title', start: 'top 84%' } }
  );

  gsap.fromTo('.vc-field__point',
    { opacity: 0, x: 24 },
    { opacity: 1, x: 0, stagger: .1, duration: .6, ease: 'power3.out',
      scrollTrigger: { trigger: '.vc-field__points', start: 'top 82%' } }
  );

  gsap.fromTo('.vc-area',
    { opacity: 0, y: 28 },
    { opacity: 1, y: 0, stagger: .12, duration: .7, ease: 'power3.out',
      scrollTrigger: { trigger: '.vc-areas__grid', start: 'top 82%' } }
  );

  gsap.fromTo('.vc-card',
    { opacity: 0, y: 24 },
    { opacity: 1, y: 0, stagger: .1, duration: .65, ease: 'power3.out',
      scrollTrigger: { trigger: '.vc-listings-section__grid', start: 'top 84%' } }
  );

  initCanvas();
}

function initCanvas() {
  var canvas = document.getElementById('blueprintCanvas');
  if (!canvas) return;

  var ctx = canvas.getContext('2d');
  var progress = 0;
  var active = false;

  function resize() {
    var r = canvas.getBoundingClientRect();
    var dpr = window.devicePixelRatio || 1;
    canvas.width = r.width * dpr;
    canvas.height = r.height * dpr;
    ctx.scale(dpr, dpr);
  }

  function W() { return canvas.getBoundingClientRect().width; }
  function H() { return canvas.getBoundingClientRect().height; }

  function lines() {
    var w = W(), h = H(), p = 22;
    return [
      { x1: p, y1: p, x2: w - p, y2: p },
      { x1: w - p, y1: p, x2: w - p, y2: h - p },
      { x1: w - p, y1: h - p, x2: p, y2: h - p },
      { x1: p, y1: h - p, x2: p, y2: p },
      { x1: p + (w - p * 2) * .52, y1: p, x2: p + (w - p * 2) * .52, y2: h * .58 },
      { x1: p, y1: h * .58, x2: w - p, y2: h * .58 },
      { x1: p + (w - p * 2) * .28, y1: h * .58, x2: p + (w - p * 2) * .28, y2: h - p },
      { x1: p + (w - p * 2) * .08, y1: p, x2: p + (w - p * 2) * .4, y2: p, col: '#DF8344', lw: 2.5 },
      { x1: p + (w - p * 2) * .6, y1: p, x2: p + (w - p * 2) * .9, y2: p, col: '#DF8344', lw: 2.5 },
      { x1: p, y1: p - 10, x2: w - p, y2: p - 10, col: 'rgba(143,168,155,0.2)', dash: [4, 4] }
    ];
  }

  function draw(prog) {
    var w = W(), h = H();
    ctx.clearRect(0, 0, w, h);

    ctx.strokeStyle = 'rgba(143,168,155,0.08)';
    ctx.lineWidth = .5;
    for (var x = 0; x < w; x += 20) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
    for (var y = 0; y < h; y += 20) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }

    var ls = lines();
    ls.forEach(function (ln, i) {
      var lp = Math.max(0, Math.min(1, (prog * ls.length) - i));
      if (lp <= 0) return;
      ctx.beginPath();
      ctx.moveTo(ln.x1, ln.y1);
      ctx.lineTo(ln.x1 + (ln.x2 - ln.x1) * lp, ln.y1 + (ln.y2 - ln.y1) * lp);
      ctx.strokeStyle = ln.col || 'rgba(143,168,155,0.45)';
      ctx.lineWidth = ln.lw || 1.5;
      ctx.setLineDash(ln.dash || []);
      ctx.stroke();
      if (lp >= 1) {
        ctx.fillStyle = ln.col || 'rgba(143,168,155,0.45)';
        ctx.beginPath();
        ctx.arc(ln.x2, ln.y2, 2, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    if (prog < 1) {
      var idx = Math.min(Math.floor(prog * ls.length), ls.length - 1);
      var cur = ls[idx];
      var fp = (prog * ls.length) % 1;
      ctx.fillStyle = '#DF8344';
      ctx.beginPath();
      ctx.arc(cur.x1 + (cur.x2 - cur.x1) * fp, cur.y1 + (cur.y2 - cur.y1) * fp, 3, 0, Math.PI * 2);
      ctx.fill();
    }
  }

  function tick() {
    progress += .004;
    draw(progress);
    if (progress < 1) requestAnimationFrame(tick);
    else active = false;
  }

  function start() {
    if (active) return;
    active = true;
    progress = 0;
    tick();
  }

  resize();
  window.addEventListener('resize', function () { resize(); draw(progress); });

  new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) start(); });
  }, { threshold: .25 }).observe(canvas);

  setInterval(function () { if (!active) start(); }, 7000);
}

function fallback() {
  new IntersectionObserver(function (entries) {
    entries.forEach(function (e) { if (e.isIntersecting) e.target.classList.add('vc-visible'); });
  }, { threshold: .1 }).observe(document.querySelectorAll('[data-reveal]'));

  document.querySelectorAll('.vc-word').forEach(function (w) { w.style.transform = 'none'; });
  ['#vcEye', '#vcSub', '#vcSearch'].forEach(function (s) {
    var el = document.querySelector(s);
    if (el) el.style.opacity = '1';
  });
  initCanvas();
}

if (!document.getElementById('vcPre')) startHero();
