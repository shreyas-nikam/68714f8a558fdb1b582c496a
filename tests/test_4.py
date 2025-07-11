import pytest
from definition_4018ddd709e64bfcb0f4d2e399bea079 import suggest_substantiation_method

@pytest.mark.parametrize("control_type, key_nonkey, manual_automated, risk_level, expected", [
    ("Preventative", "Key", "Manual", "High", "Re-performance"),
    ("Detective", "Non-Key", "Automated", "Medium", "Examination"),
    ("Preventative", "Key", "Manual", "Low", "Inquiry"),
    ("Detective", "Non-Key", "Automated", "High", "Re-performance / Examination"),
    ("Preventative", "Key", "Manual", "Medium", "Examination"),
])
def test_suggest_substantiation_method(control_type, key_nonkey, manual_automated, risk_level, expected):
    assert suggest_substantiation_method(control_type, key_nonkey, manual_automated, risk_level) == expected
