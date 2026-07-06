from pathlib import Path
from bs4 import BeautifulSoup
import html
import re
import shutil
import subprocess
import sys
from datetime import datetime


ROOT = Path(r"C:\Users\riesc\Documents\TCLP")
BACKUP_ROOT = ROOT / "_backups"

MOVIE_FOLDERS = {
    "0-d": "peliculas0d",
    "e": "peliculase",
    "f-k": "peliculasfk",
    "l": "peliculasl",
    "m-r": "peliculasmr",
    "s-z": "peliculassz",
}

MOVIE_LIST_FILES = {
    "0-d": ROOT / "peliculas" / "0-d.html",
    "e": ROOT / "peliculas" / "e.html",
    "f-k": ROOT / "peliculas" / "f-k.html",
    "l": ROOT / "peliculas" / "l.html",
    "m-r": ROOT / "peliculas" / "m-r.html",
    "s-z": ROOT / "peliculas" / "s-z.html",
}

DIRECTOR_FILES = {
    "a-e": ROOT / "directores" / "a-e.html",
    "f-j": ROOT / "directores" / "f-j.html",
    "k-o": ROOT / "directores" / "k-o.html",
    "p-t": ROOT / "directores" / "p-t.html",
    "u-z": ROOT / "directores" / "u-z.html",
}


GA_BLOCK = """<!-- Global site tag (gtag.js) - Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=UA-68812128-1"></script>
<script>
    window.dataLayer = window.dataLayer || [];
    function gtag() {
        dataLayer.push(arguments);
    }
    gtag("js", new Date());
    gtag("config", "UA-68812128-1");
</script>"""


FAVICONS_AND_FONTS = """
<link rel="apple-touch-icon" sizes="57x57" href="../objetos/favicons/apple-icon-57x57.png" />
<link rel="apple-touch-icon" sizes="60x60" href="../objetos/favicons/apple-icon-60x60.png" />
<link rel="apple-touch-icon" sizes="72x72" href="../objetos/favicons/apple-icon-72x72.png" />
<link rel="apple-touch-icon" sizes="76x76" href="../objetos/favicons/apple-icon-76x76.png" />
<link rel="apple-touch-icon" sizes="114x114" href="../objetos/favicons/apple-icon-114x114.png" />
<link rel="apple-touch-icon" sizes="120x120" href="../objetos/favicons/apple-icon-120x120.png" />
<link rel="apple-touch-icon" sizes="144x144" href="../objetos/favicons/apple-icon-144x144.png" />
<link rel="apple-touch-icon" sizes="152x152" href="../objetos/favicons/apple-icon-152x152.png" />
<link rel="apple-touch-icon" sizes="180x180" href="../objetos/favicons/apple-icon-180x180.png" />
<link rel="icon" type="image/png" sizes="192x192" href="../objetos/favicons/android-icon-192x192.png" />
<link rel="icon" type="image/png" sizes="32x32" href="../objetos/favicons/favicon-32x32.png" />
<link rel="icon" type="image/png" sizes="96x96" href="../objetos/favicons/favicon-96x96.png" />
<link rel="icon" type="image/png" sizes="16x16" href="../objetos/favicons/favicon-16x16.png" />
<link rel="manifest" href="../objetos/favicons/manifest.json" />

<meta name="msapplication-TileColor" content="#1f1f1f" />
<meta name="msapplication-TileImage" content="../objetos/favicons/ms-icon-144x144.png" />
<meta name="theme-color" content="#1f1f1f" />

<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet" />

<link rel="stylesheet" href="../normalize.css" />
<link rel="stylesheet" href="../styles.css" />
"""


HEADER = """
<header class="site-header">
    <a href="../index.html" class="logo-link">
        <img src="../objetos/logotipo.jpg" alt="Te cuento la película" class="logo" />
    </a>

    <div>
        <p class="site-kicker">Archivo personal de cine</p>
        <h1 class="title-1">Te cuento la película</h1>
    </div>
</header>

<nav class="main-nav" aria-label="Navegación principal">
    <div class="nav-links">
        <a href="../index.html">Portada</a>
        <a href="../peliculas/peliculas.html" class="active">Películas</a>
        <a href="../decadas/decadas.html">Años</a>
        <a href="../directores/directores.html">Directores</a>
        <a href="../novedades.html">Novedades</a>
    </div>

    <form class="site-search" role="search" data-root="../">
        <label class="sr-only" for="site-search-input">Buscar película</label>

        <input
            id="site-search-input"
            type="search"
            placeholder="Buscar película..."
            autocomplete="off"
        />

        <button type="submit" aria-label="Buscar">🔎</button>

        <div class="search-suggestions" id="search-suggestions" hidden></div>
    </form>
</nav>
"""


FOOTER = """
<footer class="site-footer">
    <div class="footer-inner">
        <div class="footer-links">
            <p class="footer-heading">Contacto y enlaces</p>

            <a href="mailto:isaiasriesco@gmail.com" class="footer-card">
                <span class="footer-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M4 6h16v12H4V6z" stroke="currentColor" stroke-width="1.8" />
                        <path d="M4 7l8 6 8-6" stroke="currentColor" stroke-width="1.8" />
                    </svg>
                </span>
                <span class="footer-card-text">
                    <strong>Comentarios y peticiones</strong>
                    <small>Escríbeme por correo</small>
                </span>
            </a>

            <a href="https://twitter.com/tecuentolapeli?lang=es" target="_blank" rel="noopener noreferrer" class="footer-card">
                <span class="footer-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M17.53 5H20l-5.39 6.16L21 19h-5.03l-3.94-4.8L7.8 19H5.33l5.76-6.58L5 5h5.16l3.56 4.36L17.53 5z" fill="currentColor" />
                    </svg>
                </span>
                <span class="footer-card-text">
                    <strong>Síguenos en Twitter / X</strong>
                    <small>Novedades y publicaciones</small>
                </span>
            </a>

            <a href="../documentacion.html" class="footer-card">
                <span class="footer-icon" aria-hidden="true">
                    <svg viewBox="0 0 24 24" fill="none">
                        <path d="M7 4h8l4 4v12H7V4z" stroke="currentColor" stroke-width="1.8" />
                        <path d="M15 4v4h4" stroke="currentColor" stroke-width="1.8" />
                        <path d="M9 12h6M9 16h6" stroke="currentColor" stroke-width="1.8" />
                    </svg>
                </span>
                <span class="footer-card-text">
                    <strong>Fuentes consultadas</strong>
                    <small>Documentación y referencias</small>
                </span>
            </a>
        </div>

        <div class="footer-brand">
            <img src="../objetos/tira.jpg" width="400" height="70" alt="Tira cinematográfica decorativa" />
            <p>Un archivo personal para quienes disfrutan recordando el cine con detalle.</p>
        </div>
    </div>
</footer>
"""


FLOATING_NAV = """
<div id="bottom"></div>

<nav class="floating-page-nav" aria-label="Navegación rápida de página">
    <a href="#top" aria-label="Volver arriba" title="Volver arriba">
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 5l-7 7h4v7h6v-7h4l-7-7z" />
        </svg>
    </a>

    <a href="#bottom" aria-label="Ir al final" title="Ir al final">
        <svg viewBox="0 0 24 24" aria-hidden="true">
            <path d="M12 19l7-7h-4V5H9v7H5l7 7z" />
        </svg>
    </a>
</nav>
"""


SEARCH_SCRIPTS = """
<script src="../vendor/fuse.min.js"></script>
<script src="../search-widget.js"></script>
"""


def add_movie(movie):
    warnings = []
    changed_files = []

    validate_movie(movie)

    title = movie["title"]
    year = movie["year"]
    director = movie["director"]
    director_index = movie.get("director_index") or build_director_index_name(director)

    slug = slugify(title)
    title_range = get_title_range(title)
    movie_folder_name = MOVIE_FOLDERS[title_range]
    movie_folder = ROOT / movie_folder_name
    movie_folder.mkdir(parents=True, exist_ok=True)

    html_filename = get_unique_filename(movie_folder, slug, year, ".html")
    html_path = movie_folder / html_filename

    poster_relative_from_movie = copy_poster(movie, slug, year)

    movie_url_from_root = f"{movie_folder_name}/{html_filename}"
    movie_href_from_sections = f"../{movie_url_from_root}"

    html_content = build_movie_html(
        movie=movie,
        director_index=director_index,
        poster_relative_from_movie=poster_relative_from_movie,
    )

    html_path.write_text(html_content, encoding="utf-8")
    changed_files.append(str(html_path.relative_to(ROOT)))

    update_movie_letter_listing(
        movie=movie,
        title_range=title_range,
        movie_href=movie_href_from_sections,
        changed_files=changed_files,
        warnings=warnings,
    )

    update_decade_listing(
        movie=movie,
        movie_href=movie_href_from_sections,
        changed_files=changed_files,
        warnings=warnings,
    )

    update_director_listing(
        movie=movie,
        director_index=director_index,
        movie_href=movie_href_from_sections,
        changed_files=changed_files,
        warnings=warnings,
    )

    rebuild_movies_json(changed_files, warnings)

    return {
        "html_path": str(html_path),
        "url": f"/site/{movie_url_from_root}",
        "changed_files": changed_files,
        "warnings": warnings,
    }


def validate_movie(movie):
    required = ["title", "year", "director", "summary"]

    for field in required:
        if not movie.get(field):
            raise ValueError(f"Falta el campo obligatorio: {field}")


def read_html(path):
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise Exception(f"No se pudo leer {path}")


def write_html(path, soup):
    backup_file(path)

    html_text = str(soup)
    path.write_text(html_text, encoding="utf-8")


def backup_file(path):
    if not path.exists():
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    relative_path = path.relative_to(ROOT)
    backup_path = BACKUP_ROOT / timestamp / relative_path
    backup_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, backup_path)


def slugify(value):
    value = normalize_for_sort(value)
    value = re.sub(r"[^a-z0-9]+", "", value)
    return value or "pelicula"


def normalize_for_sort(value):
    value = (value or "").lower().strip()

    replacements = {
        "á": "a",
        "à": "a",
        "ä": "a",
        "â": "a",
        "é": "e",
        "è": "e",
        "ë": "e",
        "ê": "e",
        "í": "i",
        "ì": "i",
        "ï": "i",
        "î": "i",
        "ó": "o",
        "ò": "o",
        "ö": "o",
        "ô": "o",
        "ú": "u",
        "ù": "u",
        "ü": "u",
        "û": "u",
        "ñ": "n",
        "ç": "c",
    }

    for old, new in replacements.items():
        value = value.replace(old, new)

    return value


def first_literal_letter_or_digit(value):
    normalized = normalize_for_sort(value)

    for char in normalized:
        if char.isalpha() or char.isdigit():
            return char

    return "z"


def get_title_range(title):
    first = first_literal_letter_or_digit(title)

    if first.isdigit() or first in "abcd":
        return "0-d"
    if first == "e":
        return "e"
    if first in "fghijk":
        return "f-k"
    if first == "l":
        return "l"
    if first in "mnopqr":
        return "m-r"

    return "s-z"


def get_letter_section_id(title):
    first = first_literal_letter_or_digit(title)

    if first.isdigit():
        return "letra0"

    return f"letra{first}"


def get_unique_filename(folder, slug, year, extension):
    filename = f"{slug}{extension}"

    if not (folder / filename).exists():
        return filename

    filename = f"{slug}{year}{extension}"

    if not (folder / filename).exists():
        return filename

    counter = 2

    while True:
        filename = f"{slug}{year}_{counter}{extension}"

        if not (folder / filename).exists():
            return filename

        counter += 1


def copy_poster(movie, slug, year):
    poster_path = movie.get("poster_path")

    if not poster_path:
        return ""

    source = Path(poster_path)

    if not source.exists():
        return ""

    extension = source.suffix.lower() or ".jpg"
    poster_filename = get_unique_filename(ROOT / "objetos", slug, year, extension)
    destination = ROOT / "objetos" / poster_filename

    shutil.copy2(source, destination)

    return f"../objetos/{poster_filename}"


def get_decade_file(year):
    try:
        y = int(year)
    except ValueError:
        return "decadas.html"

    if y <= 1930:
        return "1900-1930.html"
    if y <= 1940:
        return "1931-1940.html"
    if y <= 1950:
        return "1941-1950.html"
    if y <= 1960:
        return "1951-1960.html"
    if y <= 1970:
        return "1961-1970.html"
    if y <= 1980:
        return "1971-1980.html"
    if y <= 1990:
        return "1981-1990.html"
    if y <= 2000:
        return "1991-2000.html"
    if y <= 2010:
        return "2001-2010.html"
    if y <= 2020:
        return "2011-2020.html"

    return "2021-2030.html"


def get_decade_href(year):
    decade_file = get_decade_file(year)
    return f"../decadas/{decade_file}#{year}"


def build_director_index_name(director):
    director = clean_text(director)

    if "," in director:
        return director

    parts = director.split()

    if len(parts) <= 1:
        return director

    surname = parts[-1]
    name = " ".join(parts[:-1])

    return f"{surname}, {name}"


def get_director_range(director_index):
    first = first_literal_letter_or_digit(director_index)

    if first in "abcde":
        return "a-e"
    if first in "fghij":
        return "f-j"
    if first in "klmno":
        return "k-o"
    if first in "pqrst":
        return "p-t"

    return "u-z"


def clean_text(value):
    value = value or ""
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def build_movie_html(movie, director_index, poster_relative_from_movie):
    title = movie["title"]
    year = movie["year"]
    country = movie.get("country", "")
    original_title = movie.get("original_title", "")
    other_titles = movie.get("other_titles", "")

    decade_href = get_decade_href(year)

    title_line = original_title if original_title else title
    title_line_html = f'{html.escape(title_line)} (<a href="{decade_href}">{html.escape(year)}</a>)'

    if country:
        title_line_html += f" * {html.escape(country)}"

    other_titles_html = build_other_titles_html(other_titles)
    cover_html = build_cover_html(title, poster_relative_from_movie)
    hero_class = "movie-detail-hero" if poster_relative_from_movie else "movie-detail-hero movie-detail-hero-no-cover"

    summary_html = split_summary_into_paragraphs(movie.get("summary", ""))
    rating_html = build_rating_html(movie.get("rating", ""))

    page_title = f"{title} ({year}) - Resumen de la película"
    description = f"Resumen de la película {title} ({year})"

    return f"""<!doctype html>
<html lang="es">

<head>
    <meta charset="utf-8" />

    {GA_BLOCK}

    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />

    <title>{html.escape(page_title)}</title>
    <meta name="description" content="{html.escape(description)}" />
    <meta name="author" content="Isaías Riesco Rodríguez" />

    {FAVICONS_AND_FONTS}
</head>

<body>
    <div id="top"></div>

    {HEADER}

    <main>
        <section class="movie-detail-card">
            <div class="{hero_class}">
                {cover_html}

                <div class="movie-detail-info">
                    <h2 class="movie-detail-title">{html.escape(title)}</h2>

                    <div class="movie-meta">
                        <p><b>{title_line_html}</b>{other_titles_html}</p>
                        <p><b>Duración:</b> {html.escape(movie.get("duration", ""))}</p>
                        <p><b>Música:</b> {html.escape(movie.get("music", ""))}</p>
                        <p><b>Fotografía:</b> {html.escape(movie.get("photography", ""))}</p>
                        <p><b>Guion:</b> {html.escape(movie.get("script", ""))}</p>
                        <p><b>Dirección:</b> {html.escape(movie.get("director", ""))}</p>
                        <p><b>Intérpretes:</b> {html.escape(movie.get("cast", ""))}</p>
                    </div>
                </div>
            </div>

            <div class="movie-summary">
                {summary_html}
            </div>

            {rating_html}
        </section>
    </main>

    {FOOTER}

    {FLOATING_NAV}

    {SEARCH_SCRIPTS}
</body>

</html>
"""


def build_cover_html(title, poster_relative):
    if not poster_relative:
        return ""

    return f"""
                <div class="movie-cover">
                    <img src="{html.escape(poster_relative)}" alt="{html.escape(title)}" />
                </div>
"""


def build_other_titles_html(other_titles):
    other_titles = other_titles.strip()

    if not other_titles:
        return ""

    lines = [
        clean_text(line)
        for line in other_titles.splitlines()
        if clean_text(line)
    ]

    if not lines:
        return ""

    items = "<br>".join(
        f'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;- <i>{html.escape(line)}</i>'
        for line in lines
    )

    return f"""<br><br>
          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;También conocida como:<br>
          {items}"""


def split_summary_into_paragraphs(summary):
    blocks = re.split(r"\n\s*\n", summary.strip())
    paragraphs = []

    for block in blocks:
        text = " ".join(line.strip() for line in block.splitlines())
        text = clean_text(text)

        if text:
            paragraphs.append(f"<p>{html.escape(text)}</p>")

    return "\n                ".join(paragraphs)


def build_rating_html(rating):
    rating = str(rating or "").strip()

    try:
        value = float(rating.replace(",", "."))
    except ValueError:
        value = 0

    value = max(0, min(5, value))
    rounded = int(round(value))

    stars = ""

    for index in range(1, 6):
        class_name = "star star-filled" if index <= rounded else "star star-empty"
        stars += f'<span class="{class_name}">★</span>'

    display_value = int(value) if float(value).is_integer() else value

    return f"""
            <div class="movie-rating" aria-label="Calificación: {display_value} sobre 5">
                <span class="movie-rating-label">Calificación</span>
                <span class="movie-rating-stars" aria-hidden="true">
                    {stars}
                </span>
                <span class="movie-rating-value">{display_value}/5</span>
            </div>
"""


def make_soup_fragment(html_text):
    return BeautifulSoup(html_text, "html.parser")


def update_movie_letter_listing(movie, title_range, movie_href, changed_files, warnings):
    file_path = MOVIE_LIST_FILES[title_range]

    if not file_path.exists():
        warnings.append(f"No existe el listado de películas: {file_path}")
        return

    soup = BeautifulSoup(read_html(file_path), "html.parser")

    section_id = get_letter_section_id(movie["title"])
    letter_section = soup.find("section", id=section_id)

    if not letter_section:
        warnings.append(f"No se encontró la sección {section_id} en {file_path.name}")
        return

    ul = letter_section.find("ul", class_="movie-title-list")

    if not ul:
        warnings.append(f"No se encontró ul.movie-title-list en {file_path.name}, sección {section_id}")
        return

    if link_already_exists(ul, movie_href):
        warnings.append(f"La película ya parecía estar en {file_path.name}")
        return

    year = movie["year"]
    decade_href = get_decade_href(year)

    li_html = f'<li><a href="{movie_href}">{html.escape(movie["title"])}</a> (<a href="{decade_href}">{html.escape(year)}</a>)</li>'
    li = make_soup_fragment(li_html).find("li")

    ul.append(li)
    sort_li_by_movie_title(ul)

    write_html(file_path, soup)
    changed_files.append(str(file_path.relative_to(ROOT)))


def update_decade_listing(movie, movie_href, changed_files, warnings):
    year = movie["year"]
    decade_file = get_decade_file(year)
    file_path = ROOT / "decadas" / decade_file

    if not file_path.exists():
        warnings.append(f"No existe el listado de década: {file_path}")
        return

    soup = BeautifulSoup(read_html(file_path), "html.parser")

    listing = soup.find("div", class_="year-listing")

    if not listing:
        warnings.append(f"No se encontró div.year-listing en {file_path.name}")
        return

    article = soup.find("article", id=year)

    if not article:
        article_html = f"""
        <article class="year-group" id="{html.escape(year)}">
            <h3>{html.escape(year)}</h3>
            <ul class="movie-link-list"></ul>
        </article>
        """
        article = make_soup_fragment(article_html).find("article")
        listing.append(article)
        sort_year_groups(listing)

    ul = article.find("ul", class_="movie-link-list")

    if not ul:
        ul = soup.new_tag("ul")
        ul["class"] = "movie-link-list"
        article.append(ul)

    if link_already_exists(ul, movie_href):
        warnings.append(f"La película ya parecía estar en {file_path.name}, año {year}")
        return

    li_html = f'<li><a href="{movie_href}">{html.escape(movie["title"])}</a></li>'
    li = make_soup_fragment(li_html).find("li")

    ul.append(li)
    sort_li_by_movie_title(ul)

    write_html(file_path, soup)
    changed_files.append(str(file_path.relative_to(ROOT)))


def update_director_listing(movie, director_index, movie_href, changed_files, warnings):
    director_range = get_director_range(director_index)
    file_path = DIRECTOR_FILES[director_range]

    if not file_path.exists():
        warnings.append(f"No existe el listado de directores: {file_path}")
        return

    soup = BeautifulSoup(read_html(file_path), "html.parser")

    section_id = get_letter_section_id(director_index)
    letter_section = soup.find("section", id=section_id)

    if not letter_section:
        warnings.append(f"No se encontró la sección {section_id} en {file_path.name}")
        return

    director_card = find_director_card(letter_section, director_index)

    if not director_card:
        director_card_html = f"""
        <article class="director-card">
            <h3>{html.escape(director_index)}</h3>
            <ul class="director-movie-list"></ul>
        </article>
        """
        director_card = make_soup_fragment(director_card_html).find("article")
        director_listing = letter_section.find("div", class_="director-listing")

        if director_listing:
            director_listing.append(director_card)
            sort_director_cards(director_listing)
        else:
            letter_section.append(director_card)

    ul = director_card.find("ul", class_="director-movie-list")

    if not ul:
        ul = soup.new_tag("ul")
        ul["class"] = "director-movie-list"
        director_card.append(ul)

    if link_already_exists(ul, movie_href):
        warnings.append(f"La película ya parecía estar en {file_path.name}, director {director_index}")
        return

    year = movie["year"]
    decade_href = get_decade_href(year)

    li_html = f'<li><a href="{movie_href}">{html.escape(movie["title"])}</a> (<a href="{decade_href}">{html.escape(year)}</a>)</li>'
    li = make_soup_fragment(li_html).find("li")

    ul.append(li)
    sort_li_by_year_then_title(ul)

    write_html(file_path, soup)
    changed_files.append(str(file_path.relative_to(ROOT)))


def find_director_card(letter_section, director_index):
    wanted = normalize_for_sort(director_index)

    for article in letter_section.find_all("article", class_="director-card"):
        h3 = article.find("h3")

        if not h3:
            continue

        current = normalize_for_sort(h3.get_text(" ", strip=True))

        if current == wanted:
            return article

    return None


def link_already_exists(container, href):
    normalized_href = href.replace("\\", "/")

    for link in container.find_all("a", href=True):
        current_href = link["href"].replace("\\", "/")

        if current_href == normalized_href:
            return True

    return False


def sort_li_by_movie_title(ul):
    items = ul.find_all("li", recursive=False)

    items.sort(
        key=lambda li: normalize_for_sort(li.get_text(" ", strip=True))
    )

    for item in items:
        item.extract()

    for item in items:
        ul.append(item)


def sort_li_by_year_then_title(ul):
    items = ul.find_all("li", recursive=False)

    def sort_key(li):
        text = li.get_text(" ", strip=True)
        year_match = re.search(r"\b(18\d{2}|19\d{2}|20\d{2})\b", text)
        year = int(year_match.group(1)) if year_match else 9999
        return year, normalize_for_sort(text)

    items.sort(key=sort_key)

    for item in items:
        item.extract()

    for item in items:
        ul.append(item)


def sort_year_groups(listing):
    groups = listing.find_all("article", class_="year-group", recursive=False)

    def sort_key(article):
        try:
            return int(article.get("id", "9999"))
        except ValueError:
            return 9999

    groups.sort(key=sort_key)

    for group in groups:
        group.extract()

    for group in groups:
        listing.append(group)


def sort_director_cards(director_listing):
    cards = director_listing.find_all("article", class_="director-card", recursive=False)

    cards.sort(
        key=lambda card: normalize_for_sort(card.find("h3").get_text(" ", strip=True)) if card.find("h3") else ""
    )

    for card in cards:
        card.extract()

    for card in cards:
        director_listing.append(card)


def rebuild_movies_json(changed_files, warnings):
    script = ROOT / "tools" / "build_movies_index.py"

    if not script.exists():
        warnings.append("No se encontró tools/build_movies_index.py, no se pudo regenerar movies.json")
        return

    result = subprocess.run(
        [sys.executable, str(script)],
        cwd=str(ROOT),
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        warnings.append("Falló la regeneración de movies.json")
        warnings.append(result.stderr)
        return

    changed_files.append("movies.json")