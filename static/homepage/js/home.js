(function () {
    const strip = document.querySelector(".recommendation-strip");

    if (!strip || strip.scrollWidth <= strip.clientWidth) {
        return;
    }

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (prefersReducedMotion.matches) {
        return;
    }

    let paused = false;
    let lastFrame = null;
    const speed = 24;

    function step(timestamp) {
        if (lastFrame === null) {
            lastFrame = timestamp;
        }

        const elapsed = timestamp - lastFrame;
        lastFrame = timestamp;

        if (!paused) {
            strip.scrollLeft += (speed * elapsed) / 1000;

            if (strip.scrollLeft + strip.clientWidth >= strip.scrollWidth - 1) {
                strip.scrollLeft = 0;
            }
        }

        window.requestAnimationFrame(step);
    }

    strip.addEventListener("mouseenter", () => {
        paused = true;
    });
    strip.addEventListener("mouseleave", () => {
        paused = false;
    });
    strip.addEventListener("touchstart", () => {
        paused = true;
    }, { passive: true });
    strip.addEventListener("touchend", () => {
        paused = false;
    });
    strip.addEventListener("focusin", () => {
        paused = true;
    });
    strip.addEventListener("focusout", () => {
        paused = false;
    });

    window.requestAnimationFrame(step);
})();
