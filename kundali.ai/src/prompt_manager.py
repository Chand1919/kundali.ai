# src/prompt_manager.py
def create_aadhaar_prompt(aadhaar_number):
    return f"Verify Aadhaar (demo): {aadhaar_number}. Return mocked profile summary."

def create_pan_prompt(pan_number):
    return f"Check PAN (demo): {pan_number}. Estimate income bracket."

def aggregate_prompt(aadhaar_number, pan_number):
    return (
        f"User inputs:\nAadhaar: {aadhaar_number}\nPAN: {pan_number}\n"
        "Please generate a short explainable summary of eligibility for common welfare schemes. (Demo)"
    )
