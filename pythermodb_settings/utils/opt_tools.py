# import libs
import logging
from typing import (
    List,
    Dict,
    Literal,
    Protocol,
    Any
)
# locals
from ..models import (
    CustomProp,
    Component,
    ComponentKey,
    MixtureComposition,
    MixtureMoleFraction,
    MixtureMassFraction,
    MixtureVolumeFraction,
    MixtureMolarConcentration,
    MixtureMassConcentration,
    MixtureMolality,
    MixturePartialPressure,
    MixtureMoles,
    MixtureMass,
    MixtureVolume,
    UnitConversionFn
)
from .component_utils import set_component_id, find_component_by_id


# NOTE: logger
logger = logging.getLogger(__name__)


_DEFAULT_COMPONENT_KEYS: List[ComponentKey] = [
    'Name-State',
    'Formula-State',
    'Name-Formula-State'
]


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

            # Check if mole_fraction is provided, otherwise skip
            if component.mole_fraction is None:
                logging.warning(
                    f"Component {name_} does not have a mole fraction defined. Skipping.")
                continue

            # NOTE: Set feed specification
            feed_spec[
                set_component_id(
                    component=component,
                    component_key=component_key
                )
            ] = component.mole_fraction

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


# class UnitConversionFn(Protocol):
#     """
#     Callable unit conversion interface used by ``build_inputs``.

#     The callable must accept a numeric value, a source unit, and a target unit,
#     then return the value converted to the target unit. Callers must ensure the
#     provided conversion function supports every unit pair that may appear in the
#     equation input definitions and runtime inputs.
#     """

#     def __call__(
#         self,
#         *,
#         value: float,
#         from_unit: str,
#         to_unit: str,
#     ) -> float:
#         ...

# ! component composition


def component_composition(
        mixture_composition: MixtureComposition,
        component_keys: List[ComponentKey] | None = None,
        to_unit: str | None = None,
        unit_conversion_fn: UnitConversionFn | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> Dict[str, CustomProp]:
    """
    Set component composition for a multi-component mixture.

    Parameters
    ----------
    mixture_composition : MixtureComposition
        MixtureComposition object containing the basis and components.
    component_keys : List[ComponentKey], optional
        List of component keys to use for setting the composition. Default is ['Name-State', 'Formula-State', 'Name-Formula-State'].
    to_unit : str, optional
        Target unit for the composition values. If provided, the composition values will be converted to this unit using the provided unit_conversion_fn. Default is None.
    unit_conversion_fn : UnitConversionFn, optional
        Callable function for unit conversion. Must accept value, from_unit, and to_unit as keyword arguments and return the converted value. Required if to_unit is provided. Default is None.
    identifier_mode : Literal['normal', 'strict'], optional
        The mode of search for component identifiers. In 'normal' mode, the function will check against multiple identifiers (name-state, formula-state, name-formula, etc.). In 'strict' mode, it will not check Name and Formula. Default is 'normal'.

    Returns
    -------
    Dict[str, CustomProp]
        Dictionary with component identifiers as keys and their corresponding CustomProp objects as values, containing the composition value and unit.
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

        if component_keys is None:
            component_keys = _DEFAULT_COMPONENT_KEYS

        # NOTE: retrieve X
        res: Dict[str, CustomProp] = {}

        # iterate over components to set composition
        for comp_id, comp_composition in mixture_composition.compositions.items():
            # component
            comp_ = find_component_by_id(
                id=comp_id,
                components=mixture_composition.components,
                mode=identifier_mode,
            )
            # >> check
            if comp_ is None:
                logger.warning(
                    f"Component with id {comp_id} not found in mixture components. Skipping."
                )
                continue

            # create key based on component_key
            keys_ = [
                set_component_id(comp_, key) for key in component_keys
            ]

            # create CustomProp object for composition
            custom_prop = CustomProp(
                value=comp_composition.value,
                unit=comp_composition.unit,
            )

            # >> check
            if (
                custom_prop.value is None
            ):
                logger.warning(
                    f"Component {comp_.name} does not have a valid composition value. Skipping."
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

# ! set component composition


def set_component_composition(
        mixture_composition: MixtureComposition,
    component_keys: List[ComponentKey] | None = None,
    to_unit: str | None = None,
    unit_conversion_fn: UnitConversionFn | None = None,
    identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> Dict[str, float]:
    """
    Set component composition for a multi-component mixture.

    Parameters
    ----------
    mixture_composition : MixtureComposition
        MixtureComposition object containing the basis and components.
    component_keys : List[ComponentKey], optional
        List of component keys to use for setting the composition. Default is ['Name-State', 'Formula-State', 'Name-Formula-State'].
    to_unit : str, optional
        Target unit for the composition values. If provided, the composition values will be converted to this unit using the provided unit_conversion_fn. Default is None.
    unit_conversion_fn : UnitConversionFn, optional
        Callable function for unit conversion. Must accept value, from_unit, and to_unit as keyword arguments and return the converted value. Required if to_unit is provided. Default is None.
    identifier_mode : Literal['normal', 'strict'], optional
        The mode of search for component identifiers. In 'normal' mode, the function will check against multiple identifiers (name-state, formula-state, name-formula, etc.). In 'strict' mode, it will not check Name and Formula. Default is 'normal'.

    Returns
    -------
    Dict[str, float]
        Dictionary with component identifiers as keys and their corresponding composition values as floats.
    """
    try:
        # NOTE: call component_composition to get the composition dictionary
        composition_dict = component_composition(
            mixture_composition=mixture_composition,
            component_keys=component_keys,
            to_unit=to_unit,
            unit_conversion_fn=unit_conversion_fn,
            identifier_mode=identifier_mode
        )

        # extract values from CustomProp objects
        result_dict = {
            key: prop.value for key, prop in composition_dict.items()
        }

        return result_dict
    except Exception as e:
        logging.error(f"Failed to set component composition: {e}")
        raise

# SECTION: Config molar composition


def _set_mixture_composition(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> Dict[str, float]:
    """
    Set composition for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and their corresponding mole fractions as values.
    components : List[Component]
        List of Component objects, each with name, formula, and state attributes.
    component_keys : List[ComponentKey], optional
        List of component keys to use for setting the composition. Default is ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        The mode of search for component identifiers. In 'normal' mode, the function will check against multiple identifiers (name-state, formula-state, name-formula, etc.). In 'strict' mode, it will not check Name and Formula. Default is 'normal'.

    Returns
    -------
    Dict[str, float]
        Dictionary with component identifiers as keys and their corresponding mole fractions as values.
    """
    try:
        if component_keys is None:
            component_keys = _DEFAULT_COMPONENT_KEYS

        # NOTE: Initialize result dictionary
        result_dict: Dict[str, float] = {}

        # iterate over composition to set molar composition
        for comp_id, mole_fraction in composition.items():
            # find component by id
            comp_ = find_component_by_id(
                id=comp_id,
                components=components,
                mode=identifier_mode,
            )
            # >> check
            if comp_ is None:
                logger.warning(
                    f"Component with id {comp_id} not found in components. Skipping."
                )
                continue

            # create key based on component_key
            keys_ = [
                set_component_id(comp_, key) for key in component_keys
            ]

            # add to result dictionary
            for key in keys_:
                result_dict[key] = mole_fraction

        return result_dict
    except Exception as e:
        logging.error(f"Failed to set mixture composition: {e}")
        raise

# NOTE: mole fraction composition


def set_mixture_mole_fraction(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> MixtureMoleFraction:
    """
    Set mole fraction composition for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and their corresponding mole fractions as values.
    components : List[Component]
        List of Component objects, each with name, formula, and state attributes.
    component_keys : List[ComponentKey], optional
        List of component keys to use for setting the composition. Default is ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        The mode of search for component identifiers. In 'normal' mode, the function will check against multiple identifiers (name-state, formula-state, name-formula, etc.). In 'strict' mode, it will not check Name and Formula. Default is 'normal'.

    Returns
    -------
    MixtureMoleFraction
        Dictionary with component identifiers as keys and their corresponding mole fractions as values.
    """
    return _set_mixture_composition(
        composition=composition,
        components=components,
        component_keys=component_keys,
        identifier_mode=identifier_mode
    )

# NOTE: mass fraction composition


def set_mixture_mass_fraction(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> MixtureMassFraction:
    """
    Set mass fraction composition for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and their corresponding mass fractions as values.
    components : List[Component]
        List of Component objects, each with name, formula, and state attributes.
    component_keys : List[ComponentKey], optional
        List of component keys to use for setting the composition. Default is ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        The mode of search for component identifiers. In 'normal' mode, the function will check against multiple identifiers (name-state, formula-state, name-formula, etc.). In 'strict' mode, it will not check Name and Formula. Default is 'normal'.

    Returns
    -------
    MixtureMassFraction
        Dictionary with component identifiers as keys and their corresponding mass fractions as values.
    """
    return _set_mixture_composition(
        composition=composition,
        components=components,
        component_keys=component_keys,
        identifier_mode=identifier_mode
    )


def set_mixture_volume_fraction(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> MixtureVolumeFraction:
    """
    Set volume fraction composition for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and volume fractions as values.
    components : List[Component]
        Components used to resolve the input identifiers.
    component_keys : List[ComponentKey], optional
        Identifiers to include for each resolved component. Defaults to
        ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        Component identifier matching mode. Defaults to 'strict'.

    Returns
    -------
    MixtureVolumeFraction
        Volume fractions keyed by the requested component identifiers.
    """
    return _set_mixture_composition(
        composition=composition,
        components=components,
        component_keys=component_keys,
        identifier_mode=identifier_mode
    )


def set_mixture_molar_concentration(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> MixtureMolarConcentration:
    """
    Set molar concentration composition for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and molar concentrations as values.
    components : List[Component]
        Components used to resolve the input identifiers.
    component_keys : List[ComponentKey], optional
        Identifiers to include for each resolved component. Defaults to
        ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        Component identifier matching mode. Defaults to 'strict'.

    Returns
    -------
    MixtureMolarConcentration
        Molar concentrations keyed by the requested component identifiers.
    """
    return _set_mixture_composition(
        composition=composition,
        components=components,
        component_keys=component_keys,
        identifier_mode=identifier_mode
    )


def set_mixture_mass_concentration(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> MixtureMassConcentration:
    """
    Set mass concentration composition for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and mass concentrations as values.
    components : List[Component]
        Components used to resolve the input identifiers.
    component_keys : List[ComponentKey], optional
        Identifiers to include for each resolved component. Defaults to
        ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        Component identifier matching mode. Defaults to 'strict'.

    Returns
    -------
    MixtureMassConcentration
        Mass concentrations keyed by the requested component identifiers.
    """
    return _set_mixture_composition(
        composition=composition,
        components=components,
        component_keys=component_keys,
        identifier_mode=identifier_mode
    )


def set_mixture_molality(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> MixtureMolality:
    """
    Set molality composition for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and molalities as values.
    components : List[Component]
        Components used to resolve the input identifiers.
    component_keys : List[ComponentKey], optional
        Identifiers to include for each resolved component. Defaults to
        ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        Component identifier matching mode. Defaults to 'strict'.

    Returns
    -------
    MixtureMolality
        Molalities keyed by the requested component identifiers.
    """
    return _set_mixture_composition(
        composition=composition,
        components=components,
        component_keys=component_keys,
        identifier_mode=identifier_mode
    )


def set_mixture_partial_pressure(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> MixturePartialPressure:
    """
    Set partial pressure composition for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and partial pressures as values.
    components : List[Component]
        Components used to resolve the input identifiers.
    component_keys : List[ComponentKey], optional
        Identifiers to include for each resolved component. Defaults to
        ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        Component identifier matching mode. Defaults to 'strict'.

    Returns
    -------
    MixturePartialPressure
        Partial pressures keyed by the requested component identifiers.
    """
    return _set_mixture_composition(
        composition=composition,
        components=components,
        component_keys=component_keys,
        identifier_mode=identifier_mode
    )


def set_mixture_moles(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> MixtureMoles:
    """
    Set component moles for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and component moles as values.
    components : List[Component]
        Components used to resolve the input identifiers.
    component_keys : List[ComponentKey], optional
        Identifiers to include for each resolved component. Defaults to
        ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        Component identifier matching mode. Defaults to 'strict'.

    Returns
    -------
    MixtureMoles
        Component moles keyed by the requested component identifiers.
    """
    return _set_mixture_composition(
        composition=composition,
        components=components,
        component_keys=component_keys,
        identifier_mode=identifier_mode
    )


def set_mixture_mass(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> MixtureMass:
    """
    Set component masses for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and component masses as values.
    components : List[Component]
        Components used to resolve the input identifiers.
    component_keys : List[ComponentKey], optional
        Identifiers to include for each resolved component. Defaults to
        ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        Component identifier matching mode. Defaults to 'strict'.

    Returns
    -------
    MixtureMass
        Component masses keyed by the requested component identifiers.
    """
    return _set_mixture_composition(
        composition=composition,
        components=components,
        component_keys=component_keys,
        identifier_mode=identifier_mode
    )


def set_mixture_volume(
        composition: Dict[str, float],
        components: List[Component],
        component_keys: List[ComponentKey] | None = None,
        identifier_mode: Literal['normal', 'strict'] = 'strict'
) -> MixtureVolume:
    """
    Set component volumes for a multi-component mixture.

    Parameters
    ----------
    composition : Dict[str, float]
        Dictionary with component identifiers as keys and component volumes as values.
    components : List[Component]
        Components used to resolve the input identifiers.
    component_keys : List[ComponentKey], optional
        Identifiers to include for each resolved component. Defaults to
        ['Name-State', 'Formula-State', 'Name-Formula-State'].
    identifier_mode : Literal['normal', 'strict'], optional
        Component identifier matching mode. Defaults to 'strict'.

    Returns
    -------
    MixtureVolume
        Component volumes keyed by the requested component identifiers.
    """
    return _set_mixture_composition(
        composition=composition,
        components=components,
        component_keys=component_keys,
        identifier_mode=identifier_mode
    )
