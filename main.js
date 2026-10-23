(() => {
  const HOLD_MS = 6000;
  const FADE_MS = 1200;

  const header = document.querySelector("[data-header]");
  const year = document.querySelector("[data-year]");
  const motionRoot = document.querySelector("[data-hero-motion]");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 24);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const saveData = Boolean(navigator.connection?.saveData);
  const slowNet =
    typeof navigator.connection?.effectiveType === "string" &&
    /2g/.test(navigator.connection.effectiveType);

  const enableHeroMotion = () => {
    if (!motionRoot || prefersReducedMotion || saveData || slowNet) return;

    const slides = Array.from(motionRoot.querySelectorAll(".kb-slide"));
    if (!slides.length) return;

    slides.forEach((slide) => {
      const x = slide.getAttribute("data-object-x") || "50";
      slide.style.setProperty("--object-x", x);
    });

    // Decode first two frames before revealing the loop.
    const warm = slides.slice(0, 2).map((slide) => {
      const img = slide.querySelector("img");
      if (!img) return Promise.resolve();
      if (img.decode) {
        return img.decode().catch(() => undefined);
      }
      return Promise.resolve();
    });

    Promise.all(warm).then(() => {
      motionRoot.hidden = false;
      motionRoot.classList.add("is-ready");

      let index = 0;
      slides[0].classList.add("is-active");

      window.setInterval(() => {
        const current = slides[index];
        index = (index + 1) % slides.length;
        const next = slides[index];
        next.classList.add("is-active");
        window.setTimeout(() => current.classList.remove("is-active"), FADE_MS);
      }, HOLD_MS);
    });
  };

  const startMotion = () => {
    if ("requestIdleCallback" in window) {
      requestIdleCallback(enableHeroMotion, { timeout: 1400 });
    } else {
      window.setTimeout(enableHeroMotion, 450);
    }
  };
  startMotion();

  const observer = new IntersectionObserver(
    (entries) => {
      for (const entry of entries) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-inview");
          observer.unobserve(entry.target);
        }
      }
    },
    { threshold: 0.18, rootMargin: "0px 0px -8% 0px" }
  );

  document.querySelectorAll(".service-list li, .craft-visual").forEach((el) => observer.observe(el));
})();
