from convert_units import convert_units
from tests._approval import assert_matches_golden, format_convert_units_result

GOLDEN_FR_CONV_02_STEP_A = "rd_conv_02_g1_step_a.approved.txt"


def test_fr_conv_02_step_a_success():
    """Test ID: D-CONV-GM-01 / FR-CONV-02 — meter:2.5 golden master."""
    # Arrange
    unit = "meter"
    value = 2.5

    # Act
    result = convert_units(unit, value)

    # Assert — GREEN gate (FR-CONV-02)
    assert result["status"] == "success"
    assert result["failed_fields"] == []
    assert "conversions" in result

    # Assert — Golden Master approval
    assert_matches_golden(
        format_convert_units_result(result),
        GOLDEN_FR_CONV_02_STEP_A,
    )
