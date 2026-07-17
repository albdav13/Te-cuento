(function () {
    const form = document.getElementById("search-page-form");
    const input = document.getElementById("search-page-input");
    const resultsContainer = document.getElementById("search-results");
    const resultsTitle = document.getElementById("search-results-title");
    const resultsCount = document.getElementById("search-results-count");
    const sortSelect = document.getElementById("search-sort");

    if (!form || !input || !resultsContainer || !resultsTitle || !resultsCount || !sortSelect) {
        return;
    }

    if (typeof Fuse === "undefined") {
        resultsCount.textContent = "No se pudo cargar el buscador.";
        return;
    }

    let movies = [];
    let fuse = null;
    let lastQuery = "";
    let lastResults = [];

    fetch("movies.json")
        .then((response) => {
        if (!response.ok) {
            throw new Error("No se pudo cargar movies.json");
        }

        return response.json();
    })
        .then((data) => {
        movies = data;

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
            minMatchCharLength: 2,
            includeScore: true
        });

        const initialQuery = getQueryParam("q");

        if (initialQuery) {
            input.value = initialQuery;
            performSearch(initialQuery);
        } else {
            renderInitialState();
        }
    })
        .catch((error) => {
        console.warn("Error cargando movies.json", error);
        resultsCount.textContent = "No se pudo cargar el índice de películas.";
    });

    form.addEventListener("submit", (event) => {
        event.preventDefault();

        const query = input.value.trim();

        updateUrl(query);
        performSearch(query);
    });

    input.addEventListener("input", () => {
        const query = input.value.trim();

        updateUrl(query);
        performSearch(query);
    });

    sortSelect.addEventListener("change", () => {
        renderResults(lastResults, lastQuery);
    });

    function performSearch(query) {
        lastQuery = query;

        if (!fuse || query.length < 2) {
            lastResults = [];
            renderInitialState();
            return;
        }

        lastResults = fuse
            .search(query)
            .filter(({ item }) => explicitMatch(item, query));

        renderResults(lastResults, query);    }

    function renderInitialState() {
        resultsTitle.textContent = "Resultados";
        resultsCount.textContent = "Introduce al menos dos caracteres para buscar.";
        resultsContainer.innerHTML = `
      <div class="search-empty-state">
        <span aria-hidden="true">🎬</span>
        <p>Busca por título, director, actor, actriz o año.</p>
      </div>
    `;
    }

    function renderResults(results, query) {
        const sortedResults = sortResults(results);

        resultsTitle.textContent = `Resultados para “${query}”`;

        if (sortedResults.length === 0) {
            resultsCount.textContent = "No se encontraron películas.";
            resultsContainer.innerHTML = `
        <div class="search-empty-state">
          <span aria-hidden="true">🔎</span>
          <p>No hemos encontrado resultados para esa búsqueda.</p>
        </div>
      `;
            return;
        }

        resultsCount.textContent = `${sortedResults.length} resultado${sortedResults.length === 1 ? "" : "s"} encontrado${sortedResults.length === 1 ? "" : "s"}.`;

        resultsContainer.innerHTML = sortedResults
            .map(({ item }) => buildResultCard(item))
            .join("");
    }

    function sortResults(results) {
        const sortValue = sortSelect.value;
        const copy = [...results];

        if (sortValue === "title") {
            copy.sort((a, b) => normalize(a.item.title).localeCompare(normalize(b.item.title), "es"));
        }

        if (sortValue === "year-desc") {
            copy.sort((a, b) => getYear(b.item) - getYear(a.item));
        }

        if (sortValue === "year-asc") {
            copy.sort((a, b) => getYear(a.item) - getYear(b.item));
        }

        return copy;
    }

    function buildResultCard(movie) {
        const posterHtml = movie.poster
            ? `<img src="${escapeAttribute(movie.poster)}" alt="${escapeAttribute(movie.title)}" />`
            : `<span class="search-result-placeholder">🎬</span>`;

        const metaParts = [
            movie.countryYear || movie.year,
            movie.director ? `Dirección: ${movie.director}` : "",
            movie.rating ? `Calificación: ${movie.rating}` : ""
        ].filter(Boolean);

        const castHtml = movie.cast
            ? `<p class="search-result-cast"><strong>Intérpretes:</strong> ${escapeHtml(truncate(movie.cast, 180))}</p>`
            : "";

        const descriptionHtml = movie.description
            ? `<p class="search-result-description">${escapeHtml(truncate(movie.description, 220))}</p>`
            : "";

        return `
      <article class="search-result-card">
        <a class="search-result-poster" href="${escapeAttribute(movie.url)}">
          ${posterHtml}
        </a>

        <div class="search-result-info">
          <h3>
            <a href="${escapeAttribute(movie.url)}">${escapeHtml(movie.title)}</a>
          </h3>

          <p class="search-result-meta">${escapeHtml(metaParts.join(" · "))}</p>

          ${castHtml}

          ${descriptionHtml}

          <a class="search-result-link" href="${escapeAttribute(movie.url)}">Leer resumen</a>
        </div>
      </article>
    `;
    }

    function getQueryParam(name) {
        const params = new URLSearchParams(window.location.search);
        return params.get(name) || "";
    }

    function updateUrl(query) {
        const url = new URL(window.location.href);

        if (query) {
            url.searchParams.set("q", query);
        } else {
            url.searchParams.delete("q");
        }

        window.history.replaceState({}, "", url);
    }

    function getYear(movie) {
        const value = parseInt(movie.year, 10);

        if (Number.isNaN(value)) {
            return 0;
        }

        return value;
    }

    function normalize(value) {
        return String(value || "")
            .toLowerCase()
            .normalize("NFD")
            .replace(/[\u0300-\u036f]/g, "");
    }

    function truncate(value, maxLength) {
        const text = String(value || "").trim();

        if (text.length <= maxLength) {
            return text;
        }

        return text.slice(0, maxLength).trim() + "…";
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