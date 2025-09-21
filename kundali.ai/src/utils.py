# src/utils.py
import sqlite3
from datetime import datetime
import os
from config import DB_PATH, PDF_FOLDER

def init_db():
    """Initialize sqlite DB and ensure PDF folder exists."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS applicants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age INTEGER,
        dob TEXT,
        aadhaar_masked TEXT,
        pan_masked TEXT,
        ration TEXT,
        declared_assets INTEGER,
        assets_est INTEGER,
        eligibility TEXT,
        created_at TEXT
    )
    ''')
    conn.commit()
    conn.close()
    # ensure generated_pdfs folder exists
    os.makedirs(os.path.join(os.path.dirname(__file__), PDF_FOLDER), exist_ok=True)

def save_applicant(record: dict):
    """Save applicant record dict to DB. Returns inserted id."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
    INSERT INTO applicants (
        name, age, dob, aadhaar_masked, pan_masked, ration,
        declared_assets, assets_est, eligibility, created_at
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        record.get("name"),
        record.get("age"),
        record.get("dob"),
        record.get("aadhaar_masked"),
        record.get("pan_masked"),
        record.get("ration"),
        record.get("declared_assets", 0),
        record.get("assets_est", 0),
        record.get("eligibility"),
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    inserted = c.lastrowid
    conn.close()
    return inserted

def mask_id(value: str, keep_front: int = 2, keep_back: int = 2):
    """Mask an id string for safe display/storage."""
    if not value:
        return ""
    s = str(value)
    if len(s) <= keep_front + keep_back:
        return "*" * len(s)
    return s[:keep_front] + ("*" * (len(s) - keep_front - keep_back)) + s[-keep_back:]

def validate_aadhaar(aadhaar_number):
    """Return True if aadhaar is 12-digit numeric string."""
    return isinstance(aadhaar_number, str) and aadhaar_number.isdigit() and len(aadhaar_number) == 12

def validate_pan(pan_number):
    """Return True if PAN is valid (5 letters, 4 digits, 1 letter)."""
    import re
    pattern = r'^[A-Z]{5}[0-9]{4}[A-Z]$'
    return bool(re.match(pattern, str(pan_number).upper()))

def format_currency(amount: int):
    """Format integer into Indian currency like ₹1,23,456."""
    try:
        return f"₹{int(amount):,}"
    except Exception:
        return f"₹{amount}"
