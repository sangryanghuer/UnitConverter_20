from convert_units import convert_units
from tests._approval import assert_matches_golden, format_convert_units_result

GOLDEN_FR_CONV_03_STEP_A = "fr_conv_03_g1_step_a.approved.txt"


def test_fr_conv_03_step_a_success():
    """Test ID: D-CONV-02 / FR-CONV-03 — cubit:1 golden master."""
    # Arrange
    unit = "cubit"
    value = 1.0

    # Act
    result = convert_units(unit, value)

    # Assert — GREEN gate
    assert result["status"] == "success"
    assert result["failed_fields"] == []
    assert "conversions" in result

    # Assert — Golden Master approval
    assert_matches_golden(
        format_convert_units_result(result),
        GOLDEN_FR_CONV_03_STEP_A,
    )
