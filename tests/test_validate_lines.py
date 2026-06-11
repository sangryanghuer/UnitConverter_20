from convert_units import convert_units


def test_negative_value_is_fail():  # D-CONV-01
    # Arrange
    unit = "meter"
    value = -1.0

    # Act
    result = convert_units(unit, value)

    # Assert
    assert result["status"] == "invalid"
    assert result["failed_fields"] == ["value"]
    assert result["conversions"] == {}


def test_unknown_unit_is_fail():
    """Test ID: D-CONV-01 (unknown unit)
    FR: FR-CONV-01
    """
    # Arrange
    unit = "mile"
    value = 1.0

    # Act
    result = convert_units(unit, value)

    # Assert
    assert result["status"] == "invalid"
    assert result["failed_fields"] == ["unit"]
    assert result["conversions"] == {}


def test_d_conv_gm_01():
    """Test ID: D-CONV-GM-01
    FR: FR-CONV-02
    """
    # Arrange
    unit = "meter"
    value = 2.5
    expected = {
        "meter": 2.5,
        "feet": 8.2021,
        "yard": 2.7340,
        "cubit": 5.4681,
    }

    # Act
    result = convert_units(unit, value)

    # Assert
    assert result["status"] == "success"
    assert result["failed_fields"] == []
    for u, v in expected.items():
        assert round(result["conversions"][u], 4) == v


def test_d_conv_02():
    """Test ID: D-CONV-02
    FR: FR-CONV-03
    """
    # Arrange
    unit = "cubit"
    value = 1.0
    expected = {
        "meter": 0.4572,
        "feet": 1.5000,
        "yard": 0.5000,
        "cubit": 1.0,
    }

    # Act
    result = convert_units(unit, value)

    # Assert
    assert result["status"] == "success"
    assert result["failed_fields"] == []
    for u, v in expected.items():
        assert round(result["conversions"][u], 4) == v


def test_d_conv_03():
    """Test ID: D-CONV-03
    FR: FR-CONV-04
    """
    # Arrange
    unit = "feet"
    value = 1.0
    expected = {
        "meter": 0.3048,
        "feet": 1.0,
        "yard": 0.3333,
        "cubit": 0.6667,
    }

    # Act
    result = convert_units(unit, value)

    # Assert
    assert result["status"] == "success"
    assert result["failed_fields"] == []
    for u, v in expected.items():
        assert round(result["conversions"][u], 4) == v
