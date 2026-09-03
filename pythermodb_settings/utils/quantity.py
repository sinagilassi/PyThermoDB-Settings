# import libs
import logging
from collections.abc import Mapping, Sequence
from typing import Dict, Optional, List
# locals
from ..models.components import Component, ComponentKey
from ..models.quantities import ComponentAmounts, ScalarValue, ComponentValues
from ..models.conditions import CustomProp
from ..models.units import UnitConversionFn
from .quantity_tools import to_custom_props_mapping
from .component_utils import config_components_values

# NOTE: logger
logger = logging.getLogger(__name__)

# ! ::: Convert component amounts to the requested output unit


def to_amounts(
        component_amounts: ComponentAmounts,
        output_unit: Optional[str] = None,
        unit_conversion_fn: UnitConversionFn | None = None
) -> Dict[str, float]:
    """
    Convert a dictionary of component amounts to float values.

    Parameters
    ----------
    component_amounts : ComponentAmounts
        A dictionary mapping component names to amounts. Numeric values are assumed to already be in output_unit.
    output_unit : str, optional
        The unit to which CustomProp component amounts should be converted. Default is None.
    unit_conversion_fn : UnitConversionFn | None, optional
        A function to convert units of component amounts. Default is None.

    Returns
    -------
    Dict[str, float]
        A dictionary mapping component names to their respective amounts as floats.
    """
    return to_custom_props_mapping(
        values=component_amounts,
        to_unit=output_unit,
        unit_conversion_fn=unit_conversion_fn
    )


# ! ::: By order convert component amount to the requested output unit
def to_amounts_by_order(
        component_amounts: ComponentAmounts,
        components: List[Component],
        component_key: Optional[ComponentKey],
        case_sensitive: bool = True,
        sort_by_components_order: bool = True,
        output_unit: Optional[str] = None,
        unit_conversion_fn: UnitConversionFn | None = None,
) -> Optional[tuple[Dict[str, float], List[float]]]:
    """
    Convert component amounts to the requested output unit and reorder them based on the order of the components list.

    Parameters
    ----------
    component_amounts : ComponentAmounts
        A dictionary mapping component names to amounts. Numeric values are assumed to already be in output_unit.
    components : List[Component]
        A list of Component objects defining the desired order.
    component_key : ComponentKey, optional
        The key to identify components. Default is None.
    case_sensitive : bool, optional
        Whether the component names should be treated as case-sensitive. Default is True.
    sort_by_components_order : bool, optional
        Whether to sort the component amounts based on the order of the components list. Default is True.
    output_unit : str, optional
        The unit to which CustomProp component amounts should be converted. Default is None.
    unit_conversion_fn : UnitConversionFn | None, optional
        A function to convert units of component amounts. Default is None.

    Returns
    -------
    Optional[tuple[Dict[str, float], List[float]]]
        A tuple containing a dictionary mapping component names to their respective amounts as floats and a list of ordered component values. Returns None if no ordered components are found.
    """
    # SECTION: build dictionary with desired unit
    component_values = to_custom_props_mapping(
        values=component_amounts,
        to_unit=output_unit,
        unit_conversion_fn=unit_conversion_fn
    )

    # SECTION: reorder component values based on the order of components list
    ordered_component = config_components_values(
        values=component_values,
        components=components,
        component_key=component_key,
        case_sensitive=case_sensitive,
        sort_by_components_order=sort_by_components_order
    )
    # >> check
    if not ordered_component:
        return None

    return ordered_component

# ! ::: Scalar, Dict, and List Conversion Tools


def to_scalar(
        value: ScalarValue,
        name: str,
        output_unit: str | None = None,
        unit_conversion_fn: UnitConversionFn | None = None,
) -> float:
    """
    Convert a scalar numeric or CustomProp value to float.

    Parameters
    ----------
    value : ScalarValue
        A numeric value or a CustomProp instance to convert.
    name : str
        The name of the value, used for error reporting.
    output_unit : str, optional
        The unit to which a CustomProp value should be converted. Default is None.
    unit_conversion_fn : UnitConversionFn | None, optional
        A function to convert units of the value. Default is None.

    Returns
    -------
    float
        The converted scalar value as a float.

    Raises
    ------
    Exception
        If the value cannot be converted to a float.
    """
    try:
        if isinstance(value, CustomProp):
            # NOTE: extract the value and unit
            value_ = value.value
            unit_ = value.unit

            # SECTION: Convert to the desired output unit if necessary
            if (
                output_unit and
                unit_conversion_fn is not None and
                unit_.strip().lower() != output_unit.strip().lower()
            ):
                value_ = unit_conversion_fn(
                    value=value_,
                    from_unit=unit_,
                    to_unit=output_unit,
                )
            return float(value_)
        return float(value)
    except Exception as e:
        logger.error(
            "Error converting value '%s' for '%s': %s",
            value, name, e
        )
        raise


# ! ::: Dictionary Conversion Tool
def to_dict(
        values: Mapping[str, ScalarValue],
        output_unit: str | None = None,
        unit_conversion_fn: UnitConversionFn | None = None,
) -> dict[str, float]:
    """
    Convert a numeric or CustomProp mapping to a float-valued dictionary.

    Parameters
    ----------
    values : Mapping[str, ScalarValue]
        A mapping of names to numeric or CustomProp values.
    output_unit : str, optional
        The unit to which CustomProp values should be converted. Default is None.
    unit_conversion_fn : UnitConversionFn | None, optional
        A function to convert units of the values. Default is None.

    Returns
    -------
    dict[str, float]
        A dictionary mapping names to their respective values as floats.
    """
    return to_amounts(
        component_amounts=values,
        output_unit=output_unit,
        unit_conversion_fn=unit_conversion_fn,
    )


# ! ::: List Conversion Tool
def to_list(
        values: Sequence[ScalarValue],
        output_unit: str | None = None,
        unit_conversion_fn: UnitConversionFn | None = None
) -> list[float]:
    """
    Convert a numeric or CustomProp sequence to a float-valued list.

    Parameters
    ----------
    values : Sequence[ScalarValue]
        A sequence of numeric or CustomProp values.
    output_unit : str, optional
        The unit to which CustomProp values should be converted. Default is None.
    unit_conversion_fn : UnitConversionFn | None, optional
        A function to convert units of the values. Default is None.

    Returns
    -------
    list[float]
        A list of the values converted to floats.

    Raises
    ------
    TypeError
        If `values` is a string or bytes instance instead of a numeric sequence.
    """
    # ! Strings are sequences, but they are not valid numeric component inputs.
    if isinstance(values, (str, bytes)):
        raise TypeError("values must be a numeric sequence, not a string.")
    return [to_scalar(value, "values", output_unit, unit_conversion_fn) for value in values]


# ! :::Check positive scalar value


def pos(
        value: ScalarValue,
        name: str,
        output_unit: str | None = None,
        unit_conversion_fn: UnitConversionFn | None = None,
) -> float:
    """
    Convert a scalar value to float after validating it is positive.

    Parameters
    ----------
    value : ScalarValue
        A numeric value or CustomProp instance to convert and validate.
    name : str
        The name of the value used in the error message.
    output_unit : str, optional
        The unit to which a CustomProp value should be converted. Default is None.
    unit_conversion_fn : UnitConversionFn | None, optional
        A function to convert units of the value. Default is None.

    Returns
    -------
    float
        The validated scalar value as a float.

    Raises
    ------
    ValueError
        If the converted value is zero or negative.
    """
    value = to_scalar(value, name, output_unit, unit_conversion_fn)
    if value <= 0.0:
        raise ValueError(f"{name} must be greater than zero.")
    return value
