import os
import uuid
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory, url_for
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "webp", "svg"}
UPLOAD_DIR = Path(os.getenv("IMAGE_HOSTER_DIR", "./images")).resolve()

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_UPLOAD_MB", "10")) * 1024 * 1024

# Ensure the local storage folder exists at startup.
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def is_allowed_file(filename: str) -> bool:
    if "." not in filename:
        return False
    extension = filename.rsplit(".", 1)[1].lower()
    return extension in ALLOWED_EXTENSIONS


@app.get("/")
def index():
    return jsonify(
        {
            "service": "image-hoster",
            "upload_endpoint": "/upload",
            "image_endpoint": "/images/<filename>",
            "list_endpoint": "/images",
            "health_endpoint": "/health",
        }
    )


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/upload")
def upload_image():
    if "image" not in request.files:
        return jsonify({"error": "Missing file field 'image'."}), 400

    file = request.files["image"]
    if not file.filename:
        return jsonify({"error": "No file selected."}), 400

    if not is_allowed_file(file.filename):
        return (
            jsonify(
                {
                    "error": "Unsupported file type.",
                    "allowed_extensions": sorted(ALLOWED_EXTENSIONS),
                }
            ),
            400,
        )

    safe_name = secure_filename(file.filename)
    extension = safe_name.rsplit(".", 1)[1].lower()
    stored_name = f"{uuid.uuid4().hex}.{extension}"
    target_path = UPLOAD_DIR / stored_name
    file.save(target_path)

    image_url = url_for("serve_image", filename=stored_name, _external=True)
    markdown = f"![{safe_name}]({image_url})"

    return (
        jsonify(
            {
                "filename": stored_name,
                "original_filename": safe_name,
                "url": image_url,
                "markdown": markdown,
            }
        ),
        201,
    )


@app.get("/images/<path:filename>")
def serve_image(filename: str):
    return send_from_directory(UPLOAD_DIR, filename)


@app.get("/images")
def list_images():
    images = []
    for file in UPLOAD_DIR.iterdir():
        if file.is_file() and is_allowed_file(file.name):
            image_url = url_for("serve_image", filename=file.name, _external=True)
            images.append(
                {
                    "filename": file.name,
                    "url": image_url,
                    "markdown": f"![{file.name}]({image_url})",
                }
            )
    return jsonify(images)


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    app.run(host=host, port=port)