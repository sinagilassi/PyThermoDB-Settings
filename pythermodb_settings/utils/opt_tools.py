# import libs
import logging
from typing import (
    List,
    Dict,
    Callable,
    Protocol
)
# locals
from ..models import (
    CustomProp,
    Component,
    ComponentKey,
    CompositionBasis,
    CompositionReference,
    ComponentComposition,
    MixtureComposition
)
from .component_utils import set_component_id

# NOTE: logger
logger = logging.getLogger(__name__)


def set_feed_specification(
    components: List[Component],
    component_key: ComponentKey = 'Name-State',
) -> Dict[str, float]:
    """
    Set feed specification for a list of components with their mole fractions.

    Parameters
    ----------
    components : List[Component]
        List of Component objects, each with name, formula, state, and mole_fraction attributes.
    component_key : ComponentKey, optional
        Key to use for feed specification. Options are 'Name-State', 'Formula-State', 'Name-Formula', 'Name', 'Formula', 'Name-Formula-State' or 'Formula-Name-State'.

    Returns
    -------
    Dict[str, float]
        Dictionary with component identifiers as keys and their mole fractions as values.
    """
    try:
        # NOTE: Initialize feed specification dictionary
        feed_spec = {}

        # NOTE: Iterate over components to set feed specification
        for i, component in enumerate(components):
            # set
            name_ = component.name
            formula_ = component.formula
            state_ = component.state

            # Check if mole_fraction is provided, otherwise skip
            if component.mole_fraction is None:
                logging.warning(
                    f"Component {name_} does not have a mole fraction defined. Skipping.")
                continue

            # NOTE: Set feed specification
            if component_key == 'Name-State':
                feed_spec[f"{name_}-{state_}"] = component.mole_fraction
            elif component_key == 'Formula-State':
                feed_spec[f"{formula_}-{state_}"] = component.mole_fraction
            elif component_key == 'Name-Formula':
                feed_spec[f"{name_}-{formula_}"] = component.mole_fraction
            elif component_key == 'Name':
                feed_spec[name_] = component.mole_fraction
            elif component_key == 'Formula':
                feed_spec[formula_] = component.mole_fraction
            elif component_key == 'Name-Formula-State':
                feed_spec[f"{name_}-{formula_}-{state_}"] = component.mole_fraction
            elif component_key == 'Formula-Name-State':
                feed_spec[f"{formula_}-{name_}-{state_}"] = component.mole_fraction
            else:
                # raise ValueError("Invalid component_key. Use 'name' or 'formula'.")
                logging.error(
                    f"Invalid component_key: {component_key}. Use 'name' or 'formula'.")
                raise ValueError(
                    f"Invalid component_key: {component_key}. Use 'name' or 'formula'.")

        return feed_spec
    except Exception as e:
        logging.error(f"Failed to set feed specification: {e}")
        raise Exception(f"Failed to set feed specification: {e}") from e


def check_input(
    value: str | int | float
) -> int | float | str:
    """
    If value is a string that represents an int or float, convert and return the appropriate type.
    Otherwise, return value as is.
    """
    try:
        if isinstance(value, int) or isinstance(value, float):
            return value
        if isinstance(value, str):
            value_stripped = value.strip()
            # Try integer first
            try:
                return int(value_stripped)
            except ValueError:
                pass
            # Try float
            try:
                return float(value_stripped)
            except ValueError:
                pass
            # Return original string if not numeric
            return value
        return value
    except Exception as e:
        logging.error(f"Failed to detect digit/float from string: {e}")
        raise ValueError(
            f"Failed to detect digit/float from string: {e}") from e


def convert_str_numeric_to_int(
    value: str | int
) -> int | str:
    """
    Convert a string that represents an integer or float to the appropriate type.
    If the string is not numeric, return it as is.
    """
    try:
        # NOTE: check if value is integer
        if isinstance(value, int):
            return value

        # NOTE: check if value is string
        if isinstance(value, str):
            value_stripped = value.strip()
            # Try integer first
            try:
                # check it has only digits
                if value_stripped.isdigit():
                    return int(value_stripped)
                else:
                    # return original string if not numeric
                    return value
            except ValueError:
                pass
        return value  # Return original value if not a string or not numeric
    except Exception as e:
        logging.error(f"Failed to convert string to numeric: {e}")
        raise ValueError(f"Failed to convert string to numeric: {e}") from e

# SECTION: Component Composition Configuration Tools


class UnitConversionFn(Protocol):
    """
    Callable unit conversion interface used by ``build_inputs``.

    The callable must accept a numeric value, a source unit, and a target unit,
    then return the value converted to the target unit. Callers must ensure the
    provided conversion function supports every unit pair that may appear in the
    equation input definitions and runtime inputs.
    """

    def __call__(
        self,
        *,
        value: float,
        from_unit: str,
        to_unit: str,
    ) -> float:
        ...


def set_component_composition(
        mixture_composition: MixtureComposition,
        component_keys: List[ComponentKey] | None = None,
        to_unit: str | None = None,
        unit_conversion_fn: UnitConversionFn | None = None
) -> Dict[str, CustomProp]:
    """
    Set component composition for a multi-component mixture.

    Parameters
    ----------
    mixture_composition : MixtureComposition
        MixtureComposition object containing the basis and components.
    component_keys : List[ComponentKey], optional
        List of component keys to use for setting the composition. Default is ['Name-State', 'Formula-State', 'Name-Formula'].
    to_unit : str, optional
        Target unit for the composition values. If provided, the composition values will be converted to this unit using the provided unit_conversion_fn. Default is None.
    unit_conversion_fn : UnitConversionFn, optional
        Callable function for unit conversion. Must accept value, from_unit, and to_unit as keyword arguments and return the converted value. Required if to_unit is provided. Default is None.

    Returns
    -------
    Dict[str, CustomProp]
        Dictionary with component identifiers as keys and their corresponding CustomProp objects as values.
    """
    try:
        # NOTE: Validation
        if not isinstance(mixture_composition, MixtureComposition):
            raise TypeError(
                "mixture_composition must be an instance of MixtureComposition."
            )

        if (
            to_unit is not None and
            unit_conversion_fn is None
        ):
            raise ValueError(
                "unit_conversion_fn must be provided when to_unit is specified."
            )

        # set default component_keys if not provided
        if component_keys is None:
            component_keys = [
                'Name-State',
                'Formula-State',
                'Name-Formula'
            ]

        # NOTE: retrieve X
        res: Dict[str, CustomProp] = {}

        # iterate over components to set composition
        for component_composition in mixture_composition.components:
            # component
            component = component_composition.component
            # create key based on component_key
            keys_ = [
                set_component_id(component, key) for key in component_keys
            ]

            # composition
            composition_ = component.X.get('composition', {})
            # >> check if composition is valid
            if not composition_:
                logger.warning(
                    f"Component {component.name} does not have a valid composition. Skipping."
                )
                continue

            # create CustomProp object for composition
            custom_prop = CustomProp(
                value=composition_.get('value', 0),
                unit=composition_.get('unit', ''),
            )

            # >> check
            if (
                custom_prop.value is None
            ):
                logger.warning(
                    f"Component {component.name} does not have a valid composition value. Skipping."
                )
                continue

            # ! If to_unit is provided, convert the composition value to the target unit
            valid_unit = (
                custom_prop.unit is not None
                and custom_prop.unit.strip().lower() not in {"", "none", "-"}
            )

            if (
                to_unit is not None and
                unit_conversion_fn is not None and
                custom_prop.unit != to_unit and
                valid_unit
            ):
                # convert value
                converted_value = unit_conversion_fn(
                    value=custom_prop.value,
                    from_unit=custom_prop.unit,
                    to_unit=to_unit
                )
                # update custom_prop with converted value and new unit
                custom_prop.value = converted_value
                custom_prop.unit = to_unit

            # add to result dictionary
            for key in keys_:
                res[key] = custom_prop

        return res

    except Exception as e:
        logging.error(f"Failed to set component composition: {e}")
        raise
