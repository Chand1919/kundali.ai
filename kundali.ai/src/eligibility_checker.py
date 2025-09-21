# src/eligibility_checker.py
from config import ELIGIBILITY_CRITERIA

def classify_bucket(total_assets):
    """Return simple bucket name based on assets."""
    max_prop = ELIGIBILITY_CRITERIA["max_property_value"]
    if total_assets <= max_prop // 2:
        return "poor"
    if total_assets <= max_prop:
        return "lower_middle"
    if total_assets <= max_prop * 5:
        return "middle"
    return "rich"

def evaluate_eligibility(profile: dict, declared_assets: int = 0):
    """
    profile: dict with estimated_property_value, annual_income, ration_exists
    returns detailed assessment dict
    """
    prop = profile.get("estimated_property_value", 0) or 0
    income = profile.get("annual_income", 0) or 0
    ration_flag = profile.get("ration_exists", False)

    total_assets = int(prop + declared_assets)
    bucket = classify_bucket(total_assets)

    # Demo rule: poor or lower_middle or ration holder or income <= threshold => eligible
    if bucket in ("poor", "lower_middle") or ration_flag or income <= ELIGIBILITY_CRITERIA["max_income"]:
        eligibility = "eligible"
    else:
        eligibility = "not_eligible"

    score = max(0, 100 - (total_assets / 100000))
    note = f"Bucket: {bucket}. Estimated property: {prop}. Income: {income}. Ration: {ration_flag}."

    return {
        "eligibility": eligibility,
        "score": round(score, 2),
        "note": note,
        "assets_est": total_assets,
        "bucket": bucket
    }

# Keep old test-compatible function name returning boolean
def check_eligibility(user_profile: dict) -> bool:
    """
    Backwards-compatible function used by unit tests:
    Accepts a dict with 'property_value' and 'annual_income' keys.
    Returns True if eligible (simple rules).
    """
    prop = user_profile.get("property_value", 0) or 0
    income = user_profile.get("annual_income", 0) or 0
    return (prop <= ELIGIBILITY_CRITERIA["max_property_value"] and income <= ELIGIBILITY_CRITERIA["max_income"])

