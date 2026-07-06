from pathlib import Path
from bs4 import BeautifulSoup
import html


# ============================================================
# CONFIGURACIÓN
# ============================================================

# Carpeta original de tu web
SOURCE_ROOT = Path(r"C:\Users\riesc\Documents\TCLP")

# Carpeta de salida segura.
# Al principio NO sobrescribimos los originales.
OUTPUT_ROOT = Path(r"C:\Users\riesc\Documents\TCLP_modernizado")

# Carpetas donde están las páginas individuales de películas
MOVIE_FOLDERS = [
    "peliculas0d",
    "peliculase",
    "peliculasfk",
    "peliculasl",
    "peliculasmr",
    "peliculassz",
]


# ============================================================
# BLOQUES COMUNES HTML
# ============================================================

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
    <a href="../index.html">Portada</a>
    <a href="../peliculas/peliculas.html" class="active">Películas</a>
    <a href="../decadas/decadas.html">Años</a>
    <a href="../directores/directores.html">Directores</a>
    <a href="../novedades.html">Novedades</a>
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


# ============================================================
# FUNCIONES
# ============================================================

def read_html(path: Path) -> str:
    """
    Lee HTML intentando varios encodings por si hay páginas antiguas
    guardadas con codificación distinta.
    """
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise UnicodeDecodeError(
        "unknown",
        b"",
        0,
        1,
        f"No se pudo leer el archivo con utf-8, cp1252 ni latin-1: {path}"
    )

def build_rating_tag(soup: BeautifulSoup, rating_tag):
    """
    Convierte 'Calificación: 3' en un bloque visual con estrellas.
    Conserva el valor numérico original.
    """
    import re

    raw_text = rating_tag.get_text(" ", strip=True)
    match = re.search(r"(\d+(?:[,.]\d+)?)", raw_text)

    if not match:
        rating_tag["class"] = "movie-rating"
        return rating_tag

    rating_text = match.group(1).replace(",", ".")
    rating_value = float(rating_text)

    # Limitamos entre 0 y 5 por seguridad
    rating_value = max(0, min(5, rating_value))
    rounded_rating = int(round(rating_value))

    rating = soup.new_tag("div")
    rating["class"] = "movie-rating"
    rating["aria-label"] = f"Calificación: {rating_text} sobre 5"

    label = soup.new_tag("span")
    label["class"] = "movie-rating-label"
    label.string = "Calificación"

    stars = soup.new_tag("span")
    stars["class"] = "movie-rating-stars"
    stars["aria-hidden"] = "true"

    for index in range(1, 6):
        star = soup.new_tag("span")
        star["class"] = "star star-filled" if index <= rounded_rating else "star star-empty"
        star.string = "★"
        stars.append(star)

    value = soup.new_tag("span")
    value["class"] = "movie-rating-value"

    if float(rating_value).is_integer():
        value.string = f"{int(rating_value)}/5"
    else:
        value.string = f"{rating_text}/5"

    rating.append(label)
    rating.append(stars)
    rating.append(value)

    return rating

def normalize_movie_section(section) -> str:
    """
    Conserva el contenido y los textos originales, pero reorganiza visualmente:

    - Carátula a la izquierda.
    - Título y ficha técnica a la derecha.
    - Resumen debajo.
    - Calificación al final.

    No reescribe los textos de los párrafos.
    """
    section["class"] = "movie-detail-card"

    cover = section.find("div", class_="caratula")
    title = section.find("h6")
    original_rating = section.find("h5")
    rating = build_rating_tag(section, original_rating) if original_rating else None

    if cover:
        cover["class"] = "movie-cover"

    if title:
        title.name = "h2"
        title["class"] = "movie-detail-title"
    # En las páginas antiguas, los <p> directos de la sección incluyen:
    # ficha técnica primero y resumen después.
    direct_paragraphs = section.find_all("p", recursive=False)

    meta_paragraphs = []
    summary_paragraphs = []
    found_interpretes = False

    for p in direct_paragraphs:
        text = p.get_text(" ", strip=True).lower()

        if not found_interpretes:
            meta_paragraphs.append(p)

            if text.startswith("intérpretes:") or text.startswith("interpretes:"):
                found_interpretes = True
        else:
            summary_paragraphs.append(p)

    if not found_interpretes and len(direct_paragraphs) > 6:
        meta_paragraphs = direct_paragraphs[:7]
        summary_paragraphs = direct_paragraphs[7:]

    hero = section.new_tag("div")

    has_cover = bool(cover and cover.find("img"))

    if has_cover:
        hero["class"] = "movie-detail-hero"
    else:
        hero["class"] = "movie-detail-hero movie-detail-hero-no-cover"

    info = section.new_tag("div")
    info["class"] = "movie-detail-info"

    meta = section.new_tag("div")
    meta["class"] = "movie-meta"

    summary = section.new_tag("div")
    summary["class"] = "movie-summary"

    if has_cover:
        cover.extract()
        hero.append(cover)
    elif cover:
        cover.extract()

    if title:
        title.extract()
        info.append(title)

    for p in meta_paragraphs:
        p.extract()
        meta.append(p)

    info.append(meta)
    hero.append(info)

    for p in summary_paragraphs:
        p.extract()
        summary.append(p)

    if original_rating:
        original_rating.extract()

    section.clear()
    section.append(hero)
    section.append(summary)

    if rating:
        section.append(rating)

    return str(section)

def modernize_file(source_file: Path, output_file: Path):
    """
    Moderniza una página individual de película.
    """
    raw_html = read_html(source_file)
    soup = BeautifulSoup(raw_html, "html.parser")

    title_tag = soup.find("title")
    page_title = (
        title_tag.get_text(strip=True)
        if title_tag
        else "Resumen de película | Te cuento la película"
    )

    description_tag = soup.find("meta", attrs={"name": "description"})
    description = (
        description_tag.get("content", "").strip()
        if description_tag
        else ""
    )

    movie_section = soup.find("section", class_="resumen")

    if not movie_section:
        print(f"⚠️  No se encontró section.resumen en {source_file}")
        return

    movie_html = normalize_movie_section(movie_section)

    final_html = f"""<!doctype html>
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
        {movie_html}
    </main>

    {FOOTER}

    {FLOATING_NAV}
</body>

</html>
"""

    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text(final_html, encoding="utf-8")

    print(f"✅ {source_file.relative_to(SOURCE_ROOT)} → {output_file.relative_to(OUTPUT_ROOT)}")


def main():
    print("🎬 Modernizando páginas individuales de películas...")
    print(f"Origen:  {SOURCE_ROOT}")
    print(f"Destino: {OUTPUT_ROOT}")
    print("")

    total = 0

    for folder in MOVIE_FOLDERS:
        source_folder = SOURCE_ROOT / folder
        output_folder = OUTPUT_ROOT / folder

        if not source_folder.exists():
            print(f"⚠️  No existe la carpeta: {source_folder}")
            continue

        html_files = sorted(source_folder.glob("*.html"))

        if not html_files:
            print(f"⚠️  No hay HTML en: {source_folder}")
            continue

        for source_file in html_files:
            output_file = output_folder / source_file.name
            modernize_file(source_file, output_file)
            total += 1

    print("")
    print(f"✅ Proceso terminado. Páginas generadas: {total}")
    print("")
    print("Recuerda: los originales NO se han sobrescrito.")
    print(f"Revisa primero la carpeta: {OUTPUT_ROOT}")


if __name__ == "__main__":
    main()