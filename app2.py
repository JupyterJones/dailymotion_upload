from flask import Flask, request, render_template, flash, redirect, url_for, send_from_directory
import os
import subprocess
from werkzeug.utils import secure_filename
import sys
sys.path.append('/home/jack/hidden')
from KEY import CLIENT_ID, CLIENT_SECRET, USERNAME, PASSWORD, FLASK_SECRET_KEY
app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Configuration
UPLOAD_FOLDER = 'static/upload/'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov', 'mkv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500 MB

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ----------------- HELPERS -----------------
def allowed_filez(filename):
    """Check if file has a valid extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ----------------- ROUTES -----------------
@app.route("/", methods=["GET", "POST"])
def index():
    """Main page for uploading videos."""
    return render_template("index.html")

@app.route("/upload", methods=["POST", "GET"])
def upload_video():
    """Handles video upload and redirects to the title/tags input page."""
    if "file" not in request.files:
        flash("No file part")
        return redirect(url_for("index"))

    file = request.files["file"]

    if file.filename == "":
        flash("No selected file")
        return redirect(url_for("index"))

    if file and allowed_filez(file.filename):
        filename = secure_filename(file.filename)
        video_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(video_path)

        return redirect(url_for("edit_video", filename=filename))

    flash("Invalid file format")
    return redirect(url_for("index"))

@app.route("/edit/<filename>", methods=["GET", "POST"])
def edit_video(filename):
    """Displays the uploaded video and allows user to enter title and tags."""
    video_path = url_for("uploaded_file", filename=filename)

    if request.method == "POST":
        title = request.form.get("title", "Untitled Video")
        tags = request.form.get("tags", "QuikZoom, FlaskArchitect")
        
        return redirect(url_for("upload_to_dailymotion", filename=filename, title=title, tags=tags))

    return render_template("edit.html", video_path=video_path, filename=filename)

@app.route("/uploads/<filename>")
def uploaded_file(filename):
    """Serves uploaded files for preview."""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route("/upload_to_dailymotion/<filename>/<title>/<tags>", methods=["GET", "POST"])
def upload_to_dailymotion(filename, title, tags):
    """Uploads the selected video to Dailymotion."""
    full_video_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    try:
        result = subprocess.run(
            ["python", "main2.py", "--video", full_video_path, "--title", title, "--tags", tags],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            flash(f"Video '{title}' uploaded successfully!")
        else:
            flash(f"Error uploading video: {result.stderr}")

    except Exception as e:
        flash(f"Error running subprocess: {str(e)}")

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
