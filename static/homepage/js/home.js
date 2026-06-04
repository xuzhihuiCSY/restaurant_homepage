(function () {
    const strip = document.querySelector(".recommendation-strip");

    if (!strip) {
        return;
    }

    const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    if (prefersReducedMotion.matches) {
        return;
    }

    const originalCards = Array.from(strip.children);
    if (originalCards.length === 0) {
        return;
    }

    function cloneCards() {
        const clones = originalCards.map((card) => {
            const clone = card.cloneNode(true);
            clone.setAttribute("aria-hidden", "true");
            clone.classList.add("is-clone");
            strip.appendChild(clone);
            return clone;
        });

        return clones;
    }

    const firstCloneSet = cloneCards();
    const firstOriginal = originalCards[0];
    const firstClone = firstCloneSet[0];
    const cycleWidth = firstClone.offsetLeft - firstOriginal.offsetLeft;

    if (cycleWidth <= 0) {
        return;
    }

    let safetyCounter = 0;
    while (strip.scrollWidth < strip.clientWidth + cycleWidth && safetyCounter < 6) {
        cloneCards();
        safetyCounter += 1;
    }

    let paused = false;
    let lastFrame = null;
    const speed = 130;

    function step(timestamp) {
        if (lastFrame === null) {
            lastFrame = timestamp;
        }

        const elapsed = timestamp - lastFrame;
        lastFrame = timestamp;

        if (!paused) {
            strip.scrollLeft += (speed * elapsed) / 1000;

            if (strip.scrollLeft >= cycleWidth) {
                strip.scrollLeft -= cycleWidth;
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
