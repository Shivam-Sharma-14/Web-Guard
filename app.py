
from flask import Flask, render_template, request, jsonify
from scanner.controller import run_scan
from utils.report_generator import generate_pdf_report
import os
import uuid
import threading
import time

app = Flask(__name__)

REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)

# Global scan state
progress_status = {
    "progress": 0,
    "status": "Idle",
    "results": [],
    "pdf": None
}


# -------------------------
# URL Normalizer
# -------------------------
def normalize_url(url):
    url = url.strip()

    if not url.startswith("http://") and not url.startswith("https://"):
        url = "http://" + url

    return url


# -------------------------
# Background Scan Engine
# -------------------------
def background_scan(url, scan):

    try:
        url = normalize_url(url)

        progress_status["progress"] = 10
        progress_status["status"] = "Initializing Scan"
        progress_status["results"] = []
        progress_status["pdf"] = None

        time.sleep(1)

        progress_status["progress"] = 30
        progress_status["status"] = "Scanning Target"

        results = run_scan(url, scan)

        progress_status["progress"] = 80
        progress_status["status"] = "Generating Report"

        filename = f"{uuid.uuid4()}.pdf"
        path = os.path.join(REPORT_FOLDER, filename)

        generate_pdf_report(results, path, url)

        progress_status["progress"] = 100
        progress_status["status"] = "Completed"
        progress_status["results"] = results
        progress_status["pdf"] = filename

    except Exception as e:
        progress_status["progress"] = 100
        progress_status["status"] = f"Error: {str(e)}"
        progress_status["results"] = []


# -------------------------
# Routes
# -------------------------
@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")


@app.route("/start_scan", methods=["POST"])
def start_scan():

    data = request.json
    url = data.get("url")
    scan = data.get("scan")

    if not url:
        return jsonify({"error": "URL missing"}), 400

    # Reset progress
    progress_status["progress"] = 0
    progress_status["status"] = "Queued"
    progress_status["results"] = []
    progress_status["pdf"] = None

    # Start background thread
    thread = threading.Thread(target=background_scan, args=(url, scan))
    thread.daemon = True
    thread.start()

    return jsonify({"message": "Scan started"})


@app.route("/progress")
def progress():
    return jsonify(progress_status)


@app.route("/result")
def result():
    return render_template(
        "result.html",
        results=progress_status["results"],
        pdf=progress_status["pdf"]
    )


from flask import send_from_directory

@app.route("/reports/<filename>")
def download_report(filename):
    return send_from_directory("reports", filename, as_attachment=True)


# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    app.run(debug=True)

