# src/config.py
# NOTE: These endpoints & keys are placeholders. Do not attempt unauthorized scraping.
API_URLS = {
    "aadhaar_verification": "https://api.uidai.gov.in/verifyAadhaar",
    "pan_verification": "https://api.incometax.gov.in/verifyPAN",
    "property_registry": "https://property.gov.in/api/propertyDetails",
    "ration_card_verification": "https://stategov.in/api/rationCard"
}

API_KEYS = {
    "uidai": "",        # fill if you have authorized credentials
    "incometax": "",
    "property": "",
    "ration": ""
}

# Simple eligibility thresholds (demo). Tune with experts.
ELIGIBILITY_CRITERIA = {
    "max_property_value": 2_000_000,  # 20 lakh
    "max_income": 500_000             # 5 lakh
}

# DB and PDF folder
DB_PATH = "kundi.db"                  # sqlite DB in project root
PDF_FOLDER = "../web/generated_pdfs"  # relative to src/
