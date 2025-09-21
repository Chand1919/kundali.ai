# src/main.py
from flask import Flask, request, jsonify, send_from_directory
import os
from data_fetcher import fetch_aadhaar_details, fetch_pan_details, fetch_ration_details
from eligibility_checker import evaluate_eligibility
from pdf_generator import generate_pdf_report_web
from utils import mask_id, save_applicant

# Serve web/ folder statically
app = Flask(__name__, static_folder="../web", static_url_path="/")

# Ensure pdf folder exists
os.makedirs(os.path.join(app.static_folder, "generated_pdfs"), exist_ok=True)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/api/assess", methods=["POST"])
def assess():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    age = data.get("age")
    dob = data.get("dob")
    aadhaar = data.get("aadhaar", "").strip()
    pan = data.get("pan", "").strip()
    ration = data.get("ration", "").strip()
    declared_assets = int(data.get("declared_assets", 0) or 0)

    # Basic server-side validation
    if not name or len(name) < 3:
        return jsonify({"error": "Invalid name"}), 400

    # Fetch (mock or real depending on config)
    aadhaar_profile = fetch_aadhaar_details(aadhaar)
    pan_profile = fetch_pan_details(pan)
    ration_profile = fetch_ration_details(ration)

    merged = {
        "estimated_property_value": aadhaar_profile.get("estimated_property_value", 0),
        "property_count": aadhaar_profile.get("property_count", 0),
        "has_vehicle": aadhaar_profile.get("has_vehicle", False),
        "annual_income": pan_profile.get("annual_income", 0),
        "ration_exists": ration_profile.get("ration_exists", False)
    }

    assessment = evaluate_eligibility(merged, declared_assets=declared_assets)

    # Save masked record
    record = {
        "name": name,
        "age": age,
        "dob": dob,
        "aadhaar_masked": mask_id(aadhaar),
        "pan_masked": mask_id(pan),
        "ration": ration,
        "declared_assets": declared_assets,
        "assets_est": assessment.get("assets_est", 0),
        "eligibility": assessment.get("eligibility")
    }
    rec_id = save_applicant(record)

    pdf_url = generate_pdf_report_web({
        "name": name,
        "age": age,
        "dob": dob,
        "aadhaar": aadhaar,
        "pan": pan,
        "ration": ration
    }, assessment)

    return jsonify({"assessment": assessment, "pdf_url": pdf_url, "id": rec_id})

@app.route("/generated_pdfs/<path:filename>")
def serve_pdf(filename):
    return send_from_directory(os.path.join(app.static_folder, "generated_pdfs"), filename)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
