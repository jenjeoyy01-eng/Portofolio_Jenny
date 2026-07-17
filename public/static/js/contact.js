"use strict";

const contactForm = document.getElementById("contact-form");
contactForm?.addEventListener("submit", () => {
    const button = contactForm.querySelector("button[type='submit']");
    if (!button) return;
    button.disabled = true;
    button.innerHTML = '<span class="spinner"></span> Mengirim...';
});
