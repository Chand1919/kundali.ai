# src/data_fetcher.py
"""
Data fetcher with safe fallback to mocked data.
If you provide real API keys and endpoints in config.py, requests will be attempted,
otherwise functions return deterministic mock data for demo/testing.
"""
import random
import time
import requests
from config import API_URLS, API_KEYS

# ---------- Helper: deterministic-ish mock (based on input string) ----------
def _seed_from_string(s):
    return sum((ord(c) for c in str(s))) % 10

# ---------- Aadhaar fetcher ----------
def fetch_aadhaar_details(aadhaar_number: str):
    """
    Try to call configured Aadhaar API (if key present). On failure or no key,
    return mocked profile for demo.
    """
    # If API key not provided, return mock
    if not API_KEYS.get("uidai"):
        return fetch_aadhaar_details_mock(aadhaar_number)

    url = API_URLS.get("aadhaar_verification")
    headers = {"Authorization": f"Bearer {API_KEYS.get('uidai')}"}
    params = {"aadhaar": aadhaar_number}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=8)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        # fallback to mock
        return fetch_aadhaar_details_mock(aadhaar_number)

def fetch_aadhaar_details_mock(aadhaar_number: str):
    time.sleep(0.05)
    seed = _seed_from_string(aadhaar_number)
    property_count = seed % 4
    estimated_property_value = (seed * 150_000) + random.randint(0, 200_000)
    return {
        "name": f"Resident {str(aadhaar_number)[-4:]}",
        "property_count": property_count,
        "estimated_property_value": estimated_property_value,
        "has_vehicle": bool(seed % 2)
    }

# ---------- PAN fetcher ----------
def fetch_pan_details(pan_number: str):
    if not API_KEYS.get("incometax"):
        return fetch_pan_details_mock(pan_number)

    url = API_URLS.get("pan_verification")
    headers = {"Authorization": f"Bearer {API_KEYS.get('incometax')}"}
    params = {"pan": pan_number}
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=8)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return fetch_pan_details_mock(pan_number)

def fetch_pan_details_mock(pan_number: str):
    time.sleep(0.05)
    seed = _seed_from_string(pan_number)
    annual_income = (seed * 50_000) + random.randint(0, 100_000)
    return {
        "pan": pan_number,
        "annual_income": annual_income,
        "tax_paid_est": int(max(0, annual_income * 0.05))
    }

# ---------- Property fetcher (mock) ----------
def fetch_property_details(property_id: str = None):
    # For demo return a mocked property summary. Replace with real API if available.
    time.sleep(0.05)
    return {
        "property_count": random.randint(0, 3),
        "total_estimated_value": random.randint(0, 2_000_000)
    }

# ---------- Ration fetcher (mock) ----------
def fetch_ration_details(ration_number: str):
    time.sleep(0.02)
    return {
        "ration_exists": bool(ration_number),
        "household_size": random.randint(1, 8)
    }
