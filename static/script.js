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
