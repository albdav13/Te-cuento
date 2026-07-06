from pathlib import Path
from bs4 import BeautifulSoup
import json
import re


ROOT = Path(r"C:\Users\riesc\Documents\TCLP")

MOVIE_FOLDERS = [
    "peliculas0d",
    "peliculase",
    "peliculasfk",
    "peliculasl",
    "peliculasmr",
    "peliculassz",
]

OUTPUT_FILE = ROOT / "movies.json"
REPORT_FILE = ROOT / "movies_index_report.txt"


def read_html(path):
    for encoding in ("utf-8", "cp1252", "latin-1"):
        try:
            return path.read_text(encoding=encoding)
        except UnicodeDecodeError:
            continue

    raise Exception(f"No se pudo leer el archivo: {path}")


def clean_text(value):
    value = value or ""
    value = value.replace("\xa0", " ")
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def normalize_label(value):
    value = clean_text(value).lower()
    value = value.replace("á", "a")
    value = value.replace("é", "e")
    value = value.replace("í", "i")
    value = value.replace("ó", "o")
    value = value.replace("ú", "u")
    value = value.replace("ü", "u")
    value = value.replace(":", "")
    return value.strip()


def extract_year(text):
    match = re.search(r"\b(18\d{2}|19\d{2}|20\d{2})\b", text or "")
    return match.group(1) if match else ""


def get_title(section, soup, file_path):
    title_tag = section.find(["h6", "h1", "h2", "h3"])

    if title_tag:
        return clean_text(title_tag.get_text(" ", strip=True))

    title_tag = soup.find("title")

    if title_tag:
        title = clean_text(title_tag.get_text(" ", strip=True))
        title = re.split(r"\s*-\s*Resumen", title, flags=re.IGNORECASE)[0]
        title = re.sub(r"\(\d{4}\).*", "", title).strip()
        return title

    return file_path.stem


def get_poster(section):
    image_tag = section.find("img")

    if not image_tag or not image_tag.get("src"):
        return ""

    src = image_tag.get("src", "")
    src = src.replace("\\", "/")
    src = src.replace("../", "")
    src = src.lstrip("/")

    return src


def extract_label_and_value(p):
    """
    Extrae datos de párrafos tipo:
    <p><b>Dirección:</b> Paul Haggis</p>

    También intenta funcionar si el HTML está algo distinto:
    <p><strong>Dirección</strong>: Paul Haggis</p>
    <p>Dirección: Paul Haggis</p>
    """
    full_text = clean_text(p.get_text(" ", strip=True))

    bold = p.find(["b", "strong"])

    if bold:
        raw_label = clean_text(bold.get_text(" ", strip=True))
        label = normalize_label(raw_label)

        value = full_text

        # Quita del principio "Dirección:" / "Dirección"
        raw_label_clean = clean_text(raw_label).rstrip(":")
        value = re.sub(
            r"^" + re.escape(raw_label_clean) + r"\s*:?\s*",
            "",
            value,
            flags=re.IGNORECASE
        )

        return label, clean_text(value)

    match = re.match(r"^([^:]{2,35})\s*:\s*(.+)$", full_text)

    if match:
        label = normalize_label(match.group(1))
        value = clean_text(match.group(2))
        return label, value

    return "", full_text


def is_metadata_label(label):
    return label in {
        "duracion",
        "musica",
        "fotografia",
        "guion",
        "direccion",
        "interpretes",
        "calificacion"
    }


def extract_movie_data(file_path):
    raw_html = read_html(file_path)
    soup = BeautifulSoup(raw_html, "html.parser")

    section = (
            soup.find("section", class_="resumen")
            or soup.find("section", class_="movie-detail-card")
    )

    if not section:
        return None, [f"{file_path}: no se encontró section.resumen o movie-detail-card"]

    title = get_title(section, soup, file_path)

    page_title_tag = soup.find("title")
    page_title = clean_text(page_title_tag.get_text(" ", strip=True)) if page_title_tag else ""

    description_tag = soup.find("meta", attrs={"name": "description"})
    description = clean_text(description_tag.get("content", "")) if description_tag else ""

    poster = get_poster(section)

    paragraphs = section.find_all("p")

    country_year = ""
    duration = ""
    music = ""
    photography = ""
    script = ""
    director = ""
    cast = ""
    rating = ""

    issues = []

    for p in paragraphs:
        text = clean_text(p.get_text(" ", strip=True))
        label, value = extract_label_and_value(p)

        # Primer párrafo con año suele ser país/año/título original.
        # Evitamos coger años que salgan dentro del resumen.
        if not country_year and extract_year(text) and not is_metadata_label(label):
            country_year = text

        if label == "duracion":
            duration = value
        elif label == "musica":
            music = value
        elif label == "fotografia":
            photography = value
        elif label == "guion":
            script = value
        elif label == "direccion":
            director = value
        elif label == "interpretes":
            cast = value
        elif label == "calificacion":
            rating = value

    year = extract_year(country_year) or extract_year(page_title) or extract_year(description)

    if not director:
        issues.append("sin dirección")
    if not cast:
        issues.append("sin intérpretes")
    if not duration:
        issues.append("sin duración")
    if not year:
        issues.append("sin año")

    relative_url = file_path.relative_to(ROOT).as_posix()

    movie = {
        "title": title,
        "year": year,
        "countryYear": country_year,
        "director": director,
        "cast": cast,
        "duration": duration,
        "music": music,
        "photography": photography,
        "script": script,
        "rating": rating,
        "description": description,
        "url": relative_url,
        "poster": poster,
    }

    return movie, issues


def main():
    movies = []
    report_lines = []

    for folder in MOVIE_FOLDERS:
        folder_path = ROOT / folder

        if not folder_path.exists():
            report_lines.append(f"No existe la carpeta: {folder_path}")
            continue

        for file_path in sorted(folder_path.glob("*.html")):
            movie, issues = extract_movie_data(file_path)

            if not movie:
                report_lines.append(f"{file_path.relative_to(ROOT)}")
                for issue in issues:
                    report_lines.append(f"  - {issue}")
                report_lines.append("")
                continue

            movies.append(movie)

            if issues:
                report_lines.append(f"{file_path.relative_to(ROOT)} - {movie['title']}")
                for issue in issues:
                    report_lines.append(f"  - {issue}")
                report_lines.append("")

            print(f"✅ {movie['title']}")

    movies.sort(key=lambda item: item["title"].lower())

    OUTPUT_FILE.write_text(
        json.dumps(movies, ensure_ascii=False, indent=2),
        encoding="utf-8"
    )

    if report_lines:
        REPORT_FILE.write_text("\n".join(report_lines), encoding="utf-8")

    print("")
    print(f"✅ movies.json generado con {len(movies)} películas")
    print(f"📄 {OUTPUT_FILE}")

    if report_lines:
        print(f"🔎 Informe generado: {REPORT_FILE}")


if __name__ == "__main__":
    main()