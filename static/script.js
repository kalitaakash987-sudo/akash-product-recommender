document.addEventListener("DOMContentLoaded", () => {
  // Subtle reveal effect as product cards enter the viewport.
  const cards = document.querySelectorAll(".product-card");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08 });
    cards.forEach((card) => {
      card.style.opacity = "0";
      card.style.transform = "translateY(10px)";
      card.style.transition = "opacity .45s ease, transform .45s ease, border-color .25s, box-shadow .25s";
      observer.observe(card);
    });
    document.addEventListener("scroll", () => {
      document.querySelectorAll(".product-card.is-visible").forEach((card) => {
        card.style.opacity = "1";
        card.style.transform = "";
      });
    }, { passive: true });
    // Ensure cards already in view reveal even if there is no scroll.
    setTimeout(() => document.querySelectorAll(".product-card.is-visible").forEach((card) => {
      card.style.opacity = "1";
      card.style.transform = "";
    }), 80);
  }
  const slider = document.getElementById("rec_budget");
  const output = document.getElementById("budget-value");
  if (slider && output) output.textContent = "₹" + Number(slider.value).toLocaleString("en-IN");
});
/* NOVA: scroll-driven tunnel card movement */
(() => {
    const tunnel = document.querySelector("#nova-tunnel");
    if (!tunnel || tunnel.dataset.tunnelReady) return;

    tunnel.dataset.tunnelReady = "true";
    const cards = [...tunnel.querySelectorAll(".tunnel-card")];
    let progress = 0;
    let target = 0;
    let frame = null;

    function animate() {
        progress += (target - progress) * 0.09;

        cards.forEach((card, index) => {
            const offset = index / cards.length;
            const phase = (progress + offset) % 1;
            const depth = phase * 240;
            const scale = 0.55 + phase * 0.65;
            const drift = Math.sin(phase * Math.PI * 2) * 22;
            const rotate = (index % 2 ? 1 : -1) * (12 - phase * 24);

            card.style.transform =
                `translate3d(${drift}px, ${depth - 100}px, 0) ` +
                `scale(${scale}) rotate(${rotate}deg)`;

            card.style.opacity = String(
                Math.max(0.25, Math.min(1, 0.35 + phase))
            );
            card.style.zIndex = String(Math.round(phase * 10));
        });

        if (Math.abs(target - progress) > 0.001) {
            frame = requestAnimationFrame(animate);
        } else {
            frame = null;
        }
    }

    tunnel.addEventListener("wheel", (event) => {
    event.preventDefault();

    target = Math.max(
        0,
        Math.min(1, target + event.deltaY * 0.001)
    );

    if (!frame) {
        frame = requestAnimationFrame(animate);
    }
}, { passive: false });

    tunnel.addEventListener("pointermove", (event) => {
        const bounds = tunnel.getBoundingClientRect();
        const x = (event.clientX - bounds.left) / bounds.width - 0.5;
        tunnel.style.setProperty("--pointer-x", `${x * 20}px`);
    });
})();