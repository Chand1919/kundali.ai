from src.eligibility_checker import EligibilityChecker

def test_check_eligibility():
    checker = EligibilityChecker()
    assert checker.check_eligibility({"budget": 2_00_00_000})
    assert not checker.check_eligibility({"budget": 50_000})
