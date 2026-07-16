"use strict";

const sidebar = document.getElementById("admin-sidebar");
document.querySelector(".sidebar-toggle")?.addEventListener("click", () => sidebar?.classList.toggle("open"));

document.querySelectorAll("form[data-confirm]").forEach((form) => {
    form.addEventListener("submit", (event) => {
        if (!window.confirm(form.dataset.confirm || "Lanjutkan tindakan ini?")) event.preventDefault();
    });
});

document.querySelectorAll("input[type='file'][data-preview-target]").forEach((input) => {
    input.addEventListener("change", () => {
        const file = input.files?.[0];
        const target = document.querySelector(input.dataset.previewTarget);
        if (!file || !target) return;
        const reader = new FileReader();
        reader.onload = (event) => { target.src = event.target.result; };
        reader.readAsDataURL(file);
    });
});
