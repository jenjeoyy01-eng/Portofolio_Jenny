"use strict";

const flowerMenu = document.querySelector(".flower-menu");
const flowerMenuToggle = document.querySelector(".flower-menu-toggle");
const flowerDropdown = document.querySelector(".flower-dropdown");

function closeFlowerMenu() {
    flowerMenu?.classList.remove("is-open");
    flowerMenuToggle?.setAttribute("aria-expanded", "false");
}

flowerMenuToggle?.addEventListener("click", (event) => {
    event.stopPropagation();
    const isOpen = flowerMenu?.classList.toggle("is-open") ?? false;
    flowerMenuToggle.setAttribute("aria-expanded", String(isOpen));
});

flowerDropdown?.addEventListener("click", (event) => {
    if (event.target.closest("a")) {
        closeFlowerMenu();
    }
});

document.addEventListener("click", (event) => {
    if (flowerMenu && !flowerMenu.contains(event.target)) {
        closeFlowerMenu();
    }
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
        closeFlowerMenu();
        flowerMenuToggle?.focus();
    }
});

document.querySelectorAll(".flash-close").forEach((button) => {
    button.addEventListener("click", () => button.closest(".flash")?.remove());
});

const revealObserver = new IntersectionObserver(
    (entries, observer) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                entry.target.classList.add("is-visible");
                observer.unobserve(entry.target);
            }
        });
    },
    { threshold: 0.12 }
);

document.querySelectorAll(".reveal").forEach((element) => revealObserver.observe(element));
