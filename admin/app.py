from pathlib import Path
import sys

from flask import Flask, render_template, request, send_from_directory

CURRENT_DIR = Path(__file__).resolve().parent
ROOT = CURRENT_DIR.parent

sys.path.append(str(ROOT / "tools"))

from add_movie import add_movie


app = Flask(__name__)

UPLOAD_FOLDER = ROOT / "admin" / "uploads"
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)


@app.route("/", methods=["GET"])
def new_movie_form():
    return render_template("nueva_pelicula.html")


@app.route("/crear", methods=["POST"])
def create_movie():
    poster_file = request.files.get("poster")
    poster_path = None

    if poster_file and poster_file.filename:
        poster_path = UPLOAD_FOLDER / poster_file.filename
        poster_file.save(poster_path)

    movie_data = {
        "title": request.form.get("title", "").strip(),
        "original_title": request.form.get("original_title", "").strip(),
        "year": request.form.get("year", "").strip(),
        "country": request.form.get("country", "").strip(),
        "other_titles": request.form.get("other_titles", "").strip(),
        "duration": request.form.get("duration", "").strip(),
        "music": request.form.get("music", "").strip(),
        "photography": request.form.get("photography", "").strip(),
        "script": request.form.get("script", "").strip(),
        "director": request.form.get("director", "").strip(),
        "director_index": request.form.get("director_index", "").strip(),
        "cast": request.form.get("cast", "").strip(),
        "summary": request.form.get("summary", "").strip(),
        "rating": request.form.get("rating", "").strip(),
        "poster_path": poster_path,
    }

    result = add_movie(movie_data)

    changed_files_html = "".join(
        f"<li>{file}</li>"
        for file in result.get("changed_files", [])
    )

    warnings_html = "".join(
        f"<li>{warning}</li>"
        for warning in result.get("warnings", [])
    )

    return f"""
    <!doctype html>
    <html lang="es">
    <head>
        <meta charset="utf-8">
        <title>Película creada</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 900px;
                margin: 40px auto;
                padding: 0 20px;
                background: #efe6d8;
                color: #202020;
            }}

            .card {{
                background: #fffaf0;
                border: 1px solid #e4d7c1;
                border-radius: 14px;
                padding: 24px;
            }}

            h1 {{
                color: #8f261f;
            }}

            a.button {{
                display: inline-block;
                margin-top: 20px;
                padding: 12px 18px;
                border-radius: 999px;
                background: #b7352d;
                color: white;
                text-decoration: none;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>Película creada correctamente</h1>

            <p><strong>Página creada:</strong></p>
            <p>{result["html_path"]}</p>

            <p><strong>Archivos actualizados:</strong></p>
            <ul>{changed_files_html}</ul>

            {"<p><strong>Avisos:</strong></p><ul>" + warnings_html + "</ul>" if warnings_html else ""}

            <p><a href="{result["url"]}" target="_blank">Abrir la película creada</a></p>

            <a class="button" href="/">Crear otra película</a>
        </div>
    </body>
    </html>
    """

@app.route("/site/<path:filename>")
def view_site_file(filename):
    return send_from_directory(ROOT, filename)

if __name__ == "__main__":
    app.run(debug=False)