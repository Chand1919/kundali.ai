# src/pdf_generator.py
import os
from fpdf import FPDF
from config import PDF_FOLDER
from utils import mask_id
from datetime import datetime

def ensure_folder():
    os.makedirs(PDF_FOLDER, exist_ok=True)

def generate_pdf_report(user_profile: dict, eligibility_status, output_path="eligibility_report.pdf"):
    """
    Test-friendly function that creates a PDF at output_path.
    Used by unit test test_pdf_generator.py
    """
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Welfare Eligibility Report", ln=True, align="C")
    pdf.ln(6)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Name: {user_profile.get('name', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Property Value: {user_profile.get('property_value', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Annual Income: {user_profile.get('annual_income', 'N/A')}", ln=True)
    pdf.cell(0, 8, f"Eligibility Status: {'Eligible' if eligibility_status else 'Not Eligible'}", ln=True)
    pdf.output(output_path)

def generate_pdf_report_web(app_data: dict, assessment: dict):
    """
    Used by web API: generates PDF in web/generated_pdfs and returns relative URL.
    """
    ensure_folder()
    # mask Aadhaar for filename
    aad_mask = mask_id(app_data.get("aadhaar", ""), 2, 2)
    fname = f"report_{aad_mask}_{int(datetime.utcnow().timestamp())}.pdf"
    out_path = os.path.join(PDF_FOLDER, fname)

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Welfare Eligibility Report", ln=True, align="C")
    pdf.ln(6)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 8, f"Name: {app_data.get('name','N/A')}", ln=True)
    pdf.cell(0, 8, f"Age: {app_data.get('age','N/A')}", ln=True)
    pdf.cell(0, 8, f"DOB: {app_data.get('dob','N/A')}", ln=True)
    pdf.cell(0, 8, f"Aadhaar (masked): {mask_id(app_data.get('aadhaar',''),2,2)}", ln=True)
    pdf.cell(0, 8, f"PAN (masked): {mask_id(app_data.get('pan',''),2,2)}", ln=True)
    pdf.cell(0, 8, f"Ration: {app_data.get('ration','N/A')}", ln=True)
    pdf.ln(6)
    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 8, "Assessment Summary", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0,8, f"Eligibility: {assessment.get('eligibility')}", ln=True)
    pdf.cell(0,8, f"Score: {assessment.get('score')}", ln=True)
    pdf.cell(0,8, f"Estimated Total Assets (INR): {assessment.get('assets_est')}", ln=True)
    pdf.multi_cell(0,8, f"Notes: {assessment.get('note')}", align='L')
    pdf.ln(8)
    pdf.set_font("Arial", size=10)
    pdf.cell(0,8, f"Generated at: {datetime.utcnow().isoformat()} UTC", ln=True)

    pdf.output(out_path)
    return f"/generated_pdfs/{fname}"
