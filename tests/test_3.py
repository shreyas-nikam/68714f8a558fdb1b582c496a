import pytest
from definition_d557e7c7b0774e6793662cbc3f94904f import calculate_control_quality_score

@pytest.mark.parametrize("control_type, key_nonkey, manual_automated, implementation_quality_rating, expected", [
    ("Preventative", "Key", "Automated", 5, 10),
    ("Detective", "Non-Key", "Manual", 1, 1),
    ("Preventative", "Key", "Manual", 3, 6),
    ("Detective", "Key", "Automated", 4, 7),
    ("Invalid", "Key", "Automated", 4, ValueError)
])
def test_calculate_control_quality_score(control_type, key_nonkey, manual_automated, implementation_quality_rating, expected):
    try:
        if expected == ValueError:
            with pytest.raises(ValueError):
                calculate_control_quality_score(control_type, key_nonkey, manual_automated, implementation_quality_rating)
        else:
            assert calculate_control_quality_score(control_type, key_nonkey, manual_automated, implementation_quality_rating) == expected
    except Exception as e:
        assert isinstance(e, type(expected))
