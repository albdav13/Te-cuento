(function () {
    const title = document.title.replace(" | Te cuento la película", "").trim();
    const url = window.location.href;

    const whatsappLinks = document.querySelectorAll("[data-share-whatsapp]");
    const emailLinks = document.querySelectorAll("[data-share-email]");
    const copyButtons = document.querySelectorAll("[data-copy-link]");

    whatsappLinks.forEach((link) => {
        const text = `${title} - ${url}`;
        link.href = `https://wa.me/?text=${encodeURIComponent(text)}`;
    });

    emailLinks.forEach((link) => {
        const subject = title;
        const body = `Te comparto esta película de Te cuento la película:\n\n${url}`;
        link.href = `mailto:?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    });

    copyButtons.forEach((button) => {
        button.addEventListener("click", async () => {
            const container = button.closest(".movie-share");
            const feedback = container ? container.querySelector("[data-copy-feedback]") : null;

            try {
                await navigator.clipboard.writeText(url);

                if (feedback) {
                    feedback.hidden = false;

                    setTimeout(() => {
                        feedback.hidden = true;
                    }, 1800);
                }
            } catch (error) {
                window.prompt("Copia este enlace:", url);
            }
        });
    });
})();