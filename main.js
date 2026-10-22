(() => {
  const header = document.querySelector("[data-header]");
  const year = document.querySelector("[data-year]");
  const video = document.querySelector("[data-hero-video]");

  if (year) {
    year.textContent = String(new Date().getFullYear());
  }

  const onScroll = () => {
    if (!header) return;
    header.classList.toggle("is-scrolled", window.scrollY > 24);
  };
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });

  // Fast hero: poster paints first; video loads after idle / first paint.
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const saveData = navigator.connection?.saveData;
  const slowNet =
    typeof navigator.connection?.effectiveType === "string" &&
    /2g/.test(navigator.connection.effectiveType);

  const enableHeroVideo = () => {
    if (!video || prefersReducedMotion || saveData || slowNet) return;

    const start = () => {
      video.load();
      const play = video.play();
      if (play && typeof play.then === "function") {
        play
          .then(() => video.classList.add("is-ready"))
          .catch(() => {
            /* Autoplay blocked — poster remains. */
          });
      } else {
        video.classList.add("is-ready");
      }
    };

    if ("requestIdleCallback" in window) {
      requestIdleCallback(start, { timeout: 1200 });
    } else {
      window.setTimeout(start, 400);
    }
  };

  enableHeroVideo();

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
