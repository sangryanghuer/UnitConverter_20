"""Harness adapter — grid 입력을 PRD Entity API로 위임."""

from convert_units import convert_units


def validate_lines(grid):
    return convert_units(grid["unit"], grid["value"])
