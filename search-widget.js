(function () {
    console.log("Buscador: search-widget.js cargado.");

    const form = document.querySelector(".site-search");

    if (!form) {
        console.warn("Buscador: no existe .site-search en esta página.");
        return;
    }

    const input = form.querySelector('input[type="search"]');
    const suggestions = form.querySelector(".search-suggestions");
    const rootPrefix = form.dataset.root || "";

    console.log("Buscador: rootPrefix =", rootPrefix || "(raíz)");

    if (!input) {
        console.warn("Buscador: no se encontró el input de búsqueda.");
        return;
    }

    if (!suggestions) {
        console.warn("Buscador: no se encontró .search-suggestions.");
        return;
    }

    if (typeof Fuse === "undefined") {
        console.warn("Buscador: Fuse.js no está cargado. Revisa vendor/fuse.min.js.");
        return;
    }

    console.log("Buscador: Fuse.js cargado correctamente.");

    let fuse = null;
    let currentResults = [];

    fetch(rootPrefix + "movies.json")
        .then((response) => {
        console.log("Buscador: respuesta movies.json =", response.status, response.url);

        if (!response.ok) {
            throw new Error("No se pudo cargar movies.json");
        }

        return response.json();
    })
        .then((movies) => {
        console.log("Buscador: movies.json cargado:", movies.length, "películas.");

        fuse = new Fuse(movies, {
            keys: [
                { name: "title", weight: 0.45 },
                { name: "director", weight: 0.22 },
                { name: "cast", weight: 0.18 },
                { name: "description", weight: 0.10 },
                { name: "year", weight: 0.05 }
            ],
            threshold: 0.38,
            ignoreLocation: true,
            minMatchCharLength: 2
        });
    })
        .catch((error) => {
        console.warn("Buscador: error cargando movies.json.", error);
        hideSuggestions();
    });

    input.addEventListener("input", () => {
        const query = input.value.trim();

        console.log("Buscador: buscando", query);

        if (!fuse || query.length < 2) {
            hideSuggestions();
            return;
        }

        currentResults = fuse
            .search(query)
            .filter(({ item }) => explicitMatch(item, query))
            .slice(0, 7);

        console.log("Buscador: resultados", currentResults.length);

        renderSuggestions(currentResults);
    });

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const query = input.value.trim();

        if (!query) {
            return;
        }

        window.location.href = rootPrefix + "search.html?q=" + encodeURIComponent(query);
    });
    input.addEventListener("keydown", (event) => {
        if (event.key === "Escape") {
            hideSuggestions();
            input.blur();
        }
    });

    document.addEventListener("click", (event) => {
        if (!event.target.closest(".site-search")) {
            hideSuggestions();
        }
    });

    function renderSuggestions(results) {
        if (results.length === 0) {
            suggestions.innerHTML = `
        <div class="search-suggestion-empty">
          No se encontraron resultados
        </div>
      `;
            suggestions.hidden = false;
            return;
        }

        suggestions.innerHTML = results
            .map(({ item }) => {
            const posterHtml = item.poster
                ? `<img src="${rootPrefix}${escapeAttribute(item.poster)}" alt="" />`
                : `<span class="search-suggestion-placeholder">🎬</span>`;

            const meta = [
                item.countryYear || item.year,
                item.director
            ].filter(Boolean).join(" · ");

            return `
      <a class="search-suggestion-item" href="${rootPrefix}${escapeAttribute(item.url)}">
        ${posterHtml}
        <span class="search-suggestion-content">
          <strong>${escapeHtml(item.title)}</strong>
          <small>${escapeHtml(meta)}</small>
        </span>
      </a>
    `;
        })
            .join("");

        const query = input.value.trim();

        suggestions.innerHTML += `
  <a class="search-suggestion-all" href="${rootPrefix}search.html?q=${encodeURIComponent(query)}">
    Ver todos los resultados
  </a>
`;

        suggestions.hidden = false;
    }

    function hideSuggestions() {
        suggestions.hidden = true;
        suggestions.innerHTML = "";
        currentResults = [];
    }

    function escapeHtml(value) {
        return String(value || "")
            .replaceAll("&", "&amp;")
            .replaceAll("<", "&lt;")
            .replaceAll(">", "&gt;")
            .replaceAll('"', "&quot;")
            .replaceAll("'", "&#039;");
    }

    function escapeAttribute(value) {
        return escapeHtml(value);
    }

    function explicitMatch(movie, query) {
        const normalizedQuery = normalizeText(query);

        if (!normalizedQuery) {
            return false;
        }

        const searchableText = [
            movie.title,
            movie.year,
            movie.countryYear,
            movie.director,
            movie.cast,
            movie.description,
            movie.duration,
            movie.music,
            movie.photography,
            movie.script,
            movie.rating
        ]
            .filter(Boolean)
            .map(normalizeText)
            .join(" ");

        return searchableText.includes(normalizedQuery);
    }

    function normalizeText(value) {
        return String(value || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "")
            .replace(/\s+/g, " ")
            .trim();
    }
})();