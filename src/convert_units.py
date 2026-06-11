FEET_PER_METER = 3.28084
YARDS_PER_METER = 1.09361
METERS_PER_CUBIT = 0.4572

REGISTERED_UNITS = {"meter", "feet", "yard", "cubit"}

METERS_PER_UNIT = {
    "meter": 1,
    "feet": 1 / FEET_PER_METER,
    "yard": 1 / YARDS_PER_METER,
    "cubit": METERS_PER_CUBIT,
}


def _to_meters(unit, value):
    return value * METERS_PER_UNIT[unit]


def _from_meters(unit, meters):
    return round(meters / METERS_PER_UNIT[unit], 4)


def _convert_all_units(unit, value):
    meters = _to_meters(unit, value)
    return {target: _from_meters(target, meters) for target in REGISTERED_UNITS}


def _invalid_response(failed_fields):
    return {"status": "invalid", "failed_fields": failed_fields, "conversions": {}}


def _success_response(conversions):
    return {"status": "success", "failed_fields": [], "conversions": conversions}


def convert_units(unit, value):
    if value < 0:
        return _invalid_response(["value"])

    if unit not in REGISTERED_UNITS:
        return _invalid_response(["unit"])

    return _success_response(_convert_all_units(unit, value))
