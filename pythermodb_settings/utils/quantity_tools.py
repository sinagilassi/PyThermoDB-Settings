# import libs
from typing import Dict, List, Mapping, Optional, Protocol
from pythermodb_settings.models import CustomProp
# locals
from ..models.quantities import ComponentAmounts
from ..models.units import UnitConversionFn


# ! ::: Check if units match
def _same_unit(
        unit: str,
        expected_unit: str
) -> bool:
    return unit.strip().lower() == expected_unit.strip().lower()


# ! ::: Check if all CustomProp values have the expected unit
def _all_valid_units(
        values: Dict[str, CustomProp],
        expected_unit: str
) -> bool:
    if not values:
        return True

    all_units = list(set([value.unit for value in values.values()]))

    # NOTE: more than one unique unit
    if len(all_units) > 1:
        return False

    # NOTE: check if the single unit matches the expected unit
    return _same_unit(all_units[0], expected_unit)


# ! ::: Convert a CustomProp/numeric mapping to scalar values
def to_custom_props_mapping(
        values: Mapping[str, CustomProp | float | int],
        to_unit: Optional[str] = None,
        unit_conversion_fn: Optional[UnitConversionFn] = None
) -> Dict[str, float]:
    converted_values: dict[str, float] = {}

    custom_prop_values = {
        key: value
        for key, value in values.items()
        if isinstance(value, CustomProp)
    }

    # SECTION: Check all CustomProp values already use the output unit
    unit_valid = False

    # NOTE: check
    if (
        to_unit is not None and
        len(custom_prop_values) == len(values)
    ):
        unit_valid = _all_valid_units(custom_prop_values, to_unit)

    # NOTE: expected unit
    # ! just return the converted values if all units are already valid
    if unit_valid is True:
        converted_values = {
            key: float(value.value) for key, value in custom_prop_values.items()
        }

        return converted_values

    # SECTION: Convert values to the desired output unit
    for key, value in values.items():
        if isinstance(value, CustomProp):
            # NOTE: get the value and unit
            val_ = value.value
            unit_ = value.unit

            # ! to output unit
            if (
                to_unit and
                not _same_unit(unit_, to_unit) and
                unit_conversion_fn is not None
            ):
                # >>> convert
                val_ = unit_conversion_fn(
                    value=val_,
                    from_unit=unit_,
                    to_unit=to_unit
                )

            # NOTE: set
            converted_values[key] = float(val_)
        else:
            converted_values[key] = float(value)

    return converted_values


# ! ::: Convert component amounts to the requested output unit
def to_amounts(
        component_amounts: ComponentAmounts,
        output_unit: Optional[str] = None
) -> Dict[str, float]:
    """
    Convert a dictionary of component amounts to float values.

    Parameters
    ----------
    component_amounts : ComponentAmounts
        A dictionary mapping component names to amounts. Numeric values are assumed to already be in output_unit.
    output_unit : str, optional
        The unit to which CustomProp component amounts should be converted. Default is None.

    Returns
    -------
    Dict[str, float]
        A dictionary mapping component names to their respective amounts as floats.
    """
    return to_custom_props_mapping(component_amounts, output_unit)
