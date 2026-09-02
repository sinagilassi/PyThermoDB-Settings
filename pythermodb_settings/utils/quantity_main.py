# import libs
from typing import Dict, Optional, List
# locals
from ..models.components import Component, ComponentKey
from ..models.quantities import ComponentAmounts
from ..models.units import UnitConversionFn
from .quantity_tools import to_custom_props_mapping
from .component_utils import config_components_values


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
