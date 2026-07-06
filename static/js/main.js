/* APS Group — interactions. No external libraries (per design system). */
(function () {
  "use strict";

  const prefersReduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---- Sticky header: transparent over hero, solid on scroll ---- */
  const header = document.querySelector("[data-header]");
  const onScroll = () => {
    const scrolled = window.scrollY > 40;
    header.classList.toggle("is-scrolled", scrolled);
    header.classList.toggle("is-top", !scrolled);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  /* ---- Mobile drawer ---- */
  const drawer = document.querySelector("[data-drawer]");
  const openBtn = document.querySelector("[data-menu-toggle]");
  const closeEls = document.querySelectorAll("[data-menu-close]");
  const drawerLinks = document.querySelectorAll("[data-drawer-link]");

  const setDrawer = (open) => {
    drawer.classList.toggle("is-open", open);
    drawer.setAttribute("aria-hidden", open ? "false" : "true");
    openBtn.setAttribute("aria-expanded", open ? "true" : "false");
    document.body.style.overflow = open ? "hidden" : "";
  };
  if (openBtn && drawer) {
    openBtn.addEventListener("click", () => setDrawer(true));
    closeEls.forEach((el) => el.addEventListener("click", () => setDrawer(false)));
    drawerLinks.forEach((el) => el.addEventListener("click", () => setDrawer(false)));
    document.addEventListener("keydown", (e) => { if (e.key === "Escape") setDrawer(false); });
  }

  /* ---- Scroll reveal + data-anim (SAL-like, one observer, no library) ---- */
  const revealEls = document.querySelectorAll(".reveal, [data-anim]");
  // Per-element stagger: data-anim-delay="120" (ms) → transition-delay.
  revealEls.forEach((el) => {
    const d = el.getAttribute("data-anim-delay");
    if (d) el.style.transitionDelay = parseInt(d, 10) + "ms";
  });
  if (prefersReduced || !("IntersectionObserver" in window)) {
    revealEls.forEach((el) => el.classList.add("is-visible"));
  } else {
    const io = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.14, rootMargin: "0px 0px -8% 0px" });
    revealEls.forEach((el) => io.observe(el));
  }

  /* ---- Counter animation ---- */
  const counters = document.querySelectorAll("[data-count]");
  const animateCount = (el) => {
    const target = parseInt(el.getAttribute("data-count"), 10) || 0;
    if (prefersReduced) { el.textContent = target; return; }
    const duration = 1600;
    const start = performance.now();
    const step = (now) => {
      const p = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - p, 3); // easeOutCubic
      el.textContent = Math.round(eased * target);
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  if ("IntersectionObserver" in window) {
    const co = new IntersectionObserver((entries, obs) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) { animateCount(entry.target); obs.unobserve(entry.target); }
      });
    }, { threshold: 0.6 });
    counters.forEach((el) => co.observe(el));
  } else {
    counters.forEach(animateCount);
  }

  /* ---- Hero slider ---- */
  const hero = document.querySelector("[data-hero]");
  if (hero) {
    const texts = Array.from(hero.querySelectorAll("[data-slide-text]"));
    const medias = Array.from(hero.querySelectorAll("[data-slide-media]"));
    const dots = Array.from(hero.querySelectorAll("[data-dot]"));
    const count = texts.length;
    let idx = 0;
    let timer = null;
    const INTERVAL = 6000;

    const go = (n) => {
      idx = (n + count) % count;
      texts.forEach((t, i) => t.classList.toggle("is-active", i === idx));
      medias.forEach((m, i) => m.classList.toggle("is-active", i === idx));
      dots.forEach((d, i) => d.classList.toggle("is-active", i === idx));
    };
    const next = () => go(idx + 1);
    const prev = () => go(idx - 1);
    const start = () => { if (!prefersReduced) timer = setInterval(next, INTERVAL); };
    const stop = () => { if (timer) { clearInterval(timer); timer = null; } };
    const restart = () => { stop(); start(); };

    dots.forEach((d) => d.addEventListener("click", () => { go(+d.getAttribute("data-dot")); restart(); }));
    const nextBtn = hero.querySelector("[data-hero-next]");
    const prevBtn = hero.querySelector("[data-hero-prev]");
    if (nextBtn) nextBtn.addEventListener("click", () => { next(); restart(); });
    if (prevBtn) prevBtn.addEventListener("click", () => { prev(); restart(); });
    hero.addEventListener("mouseenter", stop);
    hero.addEventListener("mouseleave", start);
    start();
  }
})();
