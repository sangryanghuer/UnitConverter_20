import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from convert_units import convert_units

UNIT_ORDER = ("meter", "feet", "yard", "cubit")


def _parse_unit_value(input_str):
    if ":" not in input_str:
        return ("format", None)

    unit, value_str = input_str.split(":", 1)

    try:
        value = float(value_str)
    except ValueError:
        return ("number", value_str)

    return ("ok", (unit, value))


def main():
    input_str = input("Insert value for converting (ex: meter:2.5): ")

    kind, data = _parse_unit_value(input_str)
    if kind == "format":
        print("Invalid format. Use unit:value (ex: meter:2.5)")
        return
    if kind == "number":
        print(f"Invalid number: {data}")
        return

    unit, value = data
    result = convert_units(unit, value)

    if result["status"] == "invalid":
        if result["failed_fields"] == ["value"]:
            print("Value must be zero or positive.")
            return
        if result["failed_fields"] == ["unit"]:
            print(f"Unknown unit: {unit}")
            return

    for target in UNIT_ORDER:
        converted = result["conversions"][target]
        print(f"{value} {unit} = {converted} {target}")


if __name__ == "__main__":
    main()
