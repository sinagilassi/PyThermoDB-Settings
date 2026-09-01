# import libs
import logging
from typing import Literal, List, Optional, Dict, TypeGuard, cast, get_args, Any, Tuple
# local
from ..models import (
    Component,
    ComponentIdentity,
    ComponentKey,
    Mixture,
    MixtureIdentity,
    MixtureKey
)
from .tools import measure_time

# NOTE: logger
logger = logging.getLogger(__name__)


# ::: Create Component Identifiers :::
def create_component_id(
    component: Component,
    separator_symbol: str = '-'
) -> ComponentIdentity:
    '''
    Create component name-state and formula-state identifiers.

    Parameters
    ----------
    component : Component
        The component for which to create the identifiers.
    separator_symbol : str, optional
        The symbol to use as a separator between the name/formula and

    Returns
    -------
    ComponentIdentity
        The component identity containing name-state and formula-state
        identifiers.
    '''
    try:
        # NOTE: extract component name
        component_name = component.name.strip()
        component_formula = component.formula.strip()
        component_state = component.state.strip().lower()

        # SECTION: create component identifiers
        name_state = f"{component_name}{separator_symbol}{component_state}"
        formula_state = f"{component_formula}{separator_symbol}{component_state}"
        name_formula = f"{component_name}{separator_symbol}{component_formula}"

        return ComponentIdentity(
            name_state=name_state,
            formula_state=formula_state,
            name_formula=name_formula
        )
    except Exception as e:
        logger.error(
            f"Failed to create component identifiers for "
            f"'{component}': {e}"
        )
        raise e


def set_component_id(
    component: Component,
    component_key: ComponentKey,
    separator_symbol: str = '-',
    case: Literal['lower', 'upper', None] = None
) -> str:
    '''
    Set component identifier based on the specified key.

    Parameters
    ----------
    component : Component
        The component for which to set the identifier.
    component_key : ComponentKey
        The key to determine which identifier to use.
        Options are:
            - 'Name-State': Use the name-state identifier.
            - 'Formula-State': Use the formula-state identifier.
            - 'Name-Formula': Use the name and formula.
            - 'Name': Use the component name.
            - 'Formula': Use the component formula.
            - 'Name-Formula-State': Use the name, formula, and state.
            - 'Formula-Name-State': Use the formula, name, and state.
    separator_symbol : str, optional
        The symbol to use as a separator between the name/formula and state.
        Default is '-'.
    case : Literal['lower', 'upper', None], optional
        Convert the identifier to lower or upper case.

    Returns
    -------
    str
        The component identifier based on the specified key.
    '''
    try:
        # NOTE: create component id
        component_idx: ComponentIdentity = create_component_id(
            component=component,
            separator_symbol=separator_symbol
        )

        # init component id
        component_id: str = ""

        # NOTE: set component id
        if component_key == "Name-State":
            component_id = component_idx.name_state.strip()
        elif component_key == "Formula-State":
            component_id = component_idx.formula_state.strip()
        elif component_key == "Name-Formula":
            component_id = component_idx.name_formula.strip()
        elif component_key == "Name":
            component_id = component.name.strip()
        elif component_key == "Formula":
            component_id = component.formula.strip()
        elif component_key == "Name-Formula-State":
            component_id = f"{component_idx.name_formula.strip()}{separator_symbol}{component.state.strip().lower()}"
        elif component_key == "Formula-Name-State":
            component_id = f"{component.formula.strip()}{separator_symbol}{component.name.strip()}{separator_symbol}{component.state.strip().lower()}"
        else:
            raise ValueError(
                f"Invalid component_key '{component_key}'. "
                f"Must be one of: {', '.join(_VALID_COMPONENT_KEYS)}."
            )

        # NOTE: apply conversion
        if case == 'lower':
            component_id = component_id.lower()
        elif case == 'upper':
            component_id = component_id.upper()
        elif case is None:
            # ! do nothing
            pass
        else:
            raise ValueError(
                f"Invalid case '{case}'. "
                f"Must be 'lower', 'upper', or None."
            )

        # result
        return component_id
    except Exception as e:
        logger.error(
            f"Failed to set component identifier for "
            f"'{component}': {e}"
        )
        raise e


def create_binary_mixture_id(
    component_1: Component,
    component_2: Component,
    mixture_key: Literal[
        'Name', 'Formula'
    ] = 'Name',
    delimiter: str = "|"
) -> str:
    """Create a unique binary mixture ID based on two components.

    Parameters
    ----------
    component1 : Component
        The first component in the mixture.
    component2 : Component
        The second component in the mixture.
    component_key : Literal['Name', 'Formula'], optional
        The key to use for identifying the components, by default 'Name'.
    delimiter : str, optional
        Delimiter to separate the two components in the ID, by default "|".

    Returns
    -------
    str
        A unique binary mixture ID.

    Raises
    ------
    ValueError
        If the component_key is not recognized.

    Examples
    --------
    The following example creates a binary mixture ID for water and ethanol
    using their names:

    >>> comp1 = Component(name="Water", formula="H2O", state="l")
    >>> comp2 = Component(name="Ethanol", formula="C2H5OH", state="l")
    >>> create_binary_mixture_id(comp1, comp2, mixture_key='Name')
    'Ethanol|Water'
    """
    try:
        # SECTION: validate inputs
        # NOTE: component
        if (
            not isinstance(component_1, Component) or
            not isinstance(component_2, Component)
        ):
            raise TypeError(
                "Both component1 and component2 must be instances of Component"
            )

        # NOTE: delimiter
        if not isinstance(delimiter, str):
            raise TypeError("delimiter must be a string")
        # strip delimiter
        delimiter = delimiter.strip()

        # SECTION: get component IDs
        if mixture_key == 'Name':
            comp1_id = set_component_id(component_1, 'Name')
            comp2_id = set_component_id(component_2, 'Name')
        elif mixture_key == 'Formula':
            comp1_id = set_component_id(component_1, 'Formula')
            comp2_id = set_component_id(component_2, 'Formula')
        else:
            raise ValueError(
                "component_key must be either 'Name' or 'Formula'"
            )

        # SECTION: create unique mixture ID (sorted to ensure uniqueness)
        mixture_id = delimiter.join(sorted([comp1_id, comp2_id]))
        # strip
        mixture_id = mixture_id.strip()

        # return
        return mixture_id
    except Exception as e:
        logging.error(f"Error in create_binary_mixture_id: {e}")
        raise


def create_mixture_id(
    components: list[Component],
    mixture_key: MixtureKey = "Name",
    delimiter: str = "|",
    case: Literal['lower', 'upper', None] = None
) -> str:
    """Create a unique mixture ID based on a list of components (sorted alphabetically).

    Parameters
    ----------
    components : list[Component]
        List of components in the mixture.
    component_key : Literal['Name', 'Formula', 'Name-State', 'Formula-State', 'Name-Formula', 'Name-Formula-State', 'Formula-Name-State'], optional
        The key to use for identifying the components, by default 'Name'.
    delimiter : str, optional
        Delimiter to separate the components in the ID, by default "|".
    case : Literal['lower', 'upper', None], optional
        Convert the identifier to lower or upper case, by default 'lower'.

    Returns
    -------
    str
        A unique mixture ID.

    Raises
    ------
    ValueError
        If the component_key is not recognized.

    Examples
    --------
    The following example creates a mixture ID for water, ethanol, and methanol
    using their names:

    >>> comp1 = Component(name="Water", formula="H2O", state="l")
    >>> comp2 = Component(name="Ethanol", formula="C2H5OH", state="l")
    >>> comp3 = Component(name="Methanol", formula="CH3OH", state="l")
    >>> create_mixture_id([comp1, comp2, comp3], mixture_key='Name')
    'Ethanol|Methanol|Water'
    """
    try:
        # SECTION: validate inputs
        # NOTE: components
        if not all(isinstance(comp, Component) for comp in components):
            raise TypeError(
                "All items in components must be instances of Component"
            )
        if len(components) == 0:
            raise ValueError("components list cannot be empty")

        # NOTE: delimiter
        if not isinstance(delimiter, str):
            raise TypeError("delimiter must be a string")
        # strip delimiter
        delimiter = delimiter.strip()

        # SECTION: get component IDs
        component_ids = [
            set_component_id(
                component=comp,
                component_key=mixture_key
            )
            for comp in components
        ]

        # SECTION: create unique mixture ID (sorted to ensure uniqueness)
        # ! sorted alphabetically
        mixture_id = delimiter.join(sorted(component_ids))

        # strip
        mixture_id = mixture_id.strip()

        # NOTE: apply conversion
        if case == 'lower':
            mixture_id = mixture_id.lower()
        elif case == 'upper':
            mixture_id = mixture_id.upper()
        elif case is None:
            pass

        # return
        return mixture_id
    except Exception as e:
        logging.error(f"Error in create_mixture_id: {e}")
        raise


# ! ::: Set Component State
def set_component_state(
        component: Component,
        state: Literal['g', 'l', 's', 'aq'],
) -> Component:
    """
    Set the phase state for a single component.

    Parameters
    ----------
    component : Component
        A Component object.
    state : Literal['g', 'l', 's', 'aq']
        The desired phase state ('g' for gas, 'l' for liquid, 's' for solid, 'aq' for aqueous).

    Returns
    -------
    Component
        The Component object with the updated phase state.
    """
    try:
        # SECTION: set component state
        component.state = state
        return component
    except Exception as e:
        logger.error(f"Error setting component state: {e}")
        raise


def set_components_state(
        components: List[Component],
        state: Literal['g', 'l', 's', 'aq'],
) -> List[Component]:
    """
    Set the phase state for a list of components.

    Parameters
    ----------
    components : List[Component]
        A list of Component objects.
    state : Literal['g', 'l', 's', 'aq']
        The desired phase state ('g' for gas, 'l' for liquid, 's' for solid, 'aq' for aqueous).

    Returns
    -------
    List[Component]
        A list of Component objects with the updated phase states.
    """
    try:
        # SECTION: set components state
        updated_components = [
            set_component_state(component, state) for component in components
        ]
        return updated_components
    except Exception as e:
        logger.error(f"Error setting components state: {e}")
        raise


# SECTION: map component key
def build_component_mapper(
        component: Component,
        component_keys: Optional[List[ComponentKey]] = None
) -> Dict[ComponentKey, str]:
    '''
    Build component mapper based on the specified component keys.

    Parameters
    ----------
    component : Component
        The component for which to build the mapper.
    component_keys : Optional[List[ComponentKey]], optional
        The list of component keys to include in the mapper. If None, all keys will be included.

    Returns
    -------
    Dict[ComponentKey, str]
        A dictionary where the keys are the specified component keys and the values are the corresponding component identifiers.
    '''
    # NOTE: check if component_keys is None, if so include all keys
    if component_keys is None:
        component_keys = [
            'Name-State', 'Formula-State', 'Name-Formula', 'Name-Formula-State', 'Formula-Name-State'
        ]

    # NOTE: build mapper
    mapper = {}

    for key in component_keys:
        mapper[key] = set_component_id(
            component=component,
            component_key=key
        )

    return mapper


def build_components_mapper(
        components: List[Component],
        component_key: ComponentKey,
        component_keys: Optional[List[ComponentKey]] = None
) -> Dict[str, Dict[ComponentKey, str]]:
    '''
    Build a list of component mappers for a list of components based on the specified component keys.

    Parameters
    ----------
    components : List[Component]
        The list of components for which to build the mappers.
    component_key : ComponentKey
        The key to determine which identifier to use for the mapper.
    component_keys : Optional[List[ComponentKey]], optional
        The list of component keys to include in the mappers. If None, all keys will be included.

    Returns
    -------
    Dict[str, Dict[ComponentKey, str]]
        A list of dictionaries, where each dictionary is a mapper for a component based on the specified keys.
    '''
    # NOTE: check if component_keys is None, if so include all keys
    if component_keys is None:
        component_keys = [
            'Name-State', 'Formula-State', 'Name-Formula', 'Name-Formula-State', 'Formula-Name-State'
        ]

    # NOTE: build mappers for each component
    mappers = {}

    # create key
    mapper_keys = [
        set_component_id(
            component=component,
            component_key=component_key
        ) for component in components
    ]

    # NOTE: build mappers
    for key, component in zip(mapper_keys, components):
        mappers[key] = build_component_mapper(
            component=component,
            component_keys=component_keys
        )

    return mappers


# SECTION: type guards
_VALID_COMPONENT_KEYS = cast(tuple[str, ...], get_args(ComponentKey))


def is_component_key(value: str) -> TypeGuard[ComponentKey]:
    return value.strip() in _VALID_COMPONENT_KEYS


# SECTION: Component references
def generate_component_references(
        components: List[Component],
        component_key: ComponentKey
) -> Dict[str, Any]:
    """
    Generate component references based on the components and the component key. This method creates a mapping of component IDs, formula-state representations, and other relevant references for the components in the model source.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the generated component references, including:
        - component_num: The number of components.
        - component_ids: A list of component IDs generated based on the component key.
        - component_mapper: A dictionary mapping component IDs to their corresponding component keys for different properties.
        - component_id_to_index: A dictionary mapping component IDs to their corresponding indices in the components list.
        - component_name_state: A list of name-state representations for the components.
        - component_formula_state: A list of formula-state representations for the components.
        - component_name_formula: A list of name-formula representations for the components.
        - component_name_formula_state: A list of name-formula-state representations for the components.
    """
    # NOTE: numbers
    component_num = len(components)

    # NOTE: Create component ID list
    component_ids: list[str] = [
        set_component_id(
            component=comp,
            component_key=cast(ComponentKey, component_key)
        )
        for comp in components
    ]

    # >>> formula-state
    component_formula_state: list[str] = [
        set_component_id(
            component=component,
            component_key='Formula-State'
        )
        for component in components
    ]

    # >>> name-state
    component_name_state: list[str] = [
        set_component_id(
            component=component,
            component_key='Name-State'
        )
        for component in components
    ]

    # >>> name-formula
    component_name_formula: list[str] = [
        set_component_id(
            component=component,
            component_key='Name-Formula'
        )
        for component in components
    ]

    # >>> name-formula-state
    component_name_formula_state: list[str] = [
        set_component_id(
            component=component,
            component_key='Name-Formula-State'
        )
        for component in components
    ]

    # NOTE: build component mapper
    component_mapper: Dict[str, Dict[ComponentKey, str]] = build_components_mapper(
        components=components,
        component_key=cast(ComponentKey, component_key)
    )

    # >> index mapping
    component_id_to_index: dict[str, int] = {
        comp_id: idx for idx, comp_id in enumerate(component_ids)
    }

    return {
        "component_num": component_num,
        "component_ids": component_ids,
        "component_mapper": component_mapper,
        "component_id_to_index": component_id_to_index,
        "component_name_state": component_name_state,
        "component_formula_state": component_formula_state,
        "component_name_formula": component_name_formula,
        "component_name_formula_state": component_name_formula_state
    }


# SECTION: mixture references
def generate_mixture_references(
        mixtures: List[Mixture],
        mixture_key: MixtureKey,
        mixture_keys: Optional[List[MixtureKey]] = None,
        delimiter: str = "|",
        case: Literal['lower', 'upper'] | None = None
) -> Dict[str, Any]:
    """
    Generate mixture references based on the mixtures and the mixture key. This method creates a mapping of mixture IDs, component numbers, and other relevant references for the mixtures in the model source.

    Parameters
    ----------
    mixtures : List[Mixture]
        A list of mixtures, where each mixture is a list of Component objects.
    mixture_key : MixtureKey
        The key to determine which identifier to use for the mixture.
    mixture_keys : Optional[List[MixtureKey]], optional
        The list of mixture keys to include in the references. If None, all keys will be included.
    delimiter : str, optional
        The symbol to use as a separator between the components in the mixture ID. Default is '|'.
    case : Literal['lower', 'upper'] | None, optional
        Convert the mixture ID to lower or upper case. Default is None.

    Returns
    -------
    Dict[str, Any]
        A dictionary containing the generated mixture references, including:
        - mixture_components_num: The number of mixtures.
        - mixture_id: A list of mixture IDs generated based on the mixture key.
        - mixture_*: A list of mixture IDs for each specified key in mixture_keys.

    Notes
    -----
    - The mixture ID is created by concatenating the component identifiers of each mixture, sorted alphabetically, and separated by the specified delimiter.
    - Validation is performed to ensure that the mixtures list is not empty. If it is empty, an empty dictionary with mixture_num set to 0 and an empty mixture_id list is returned.
    - If mixture_keys is None, a default list of keys is used: ['Name', 'Formula', 'Name-State', 'Formula-State', 'Name-Formula'].
    """
    try:
        # NOTE: validation
        if len(mixtures) == 0:
            return {}

        # NOTE: create mixture id
        mixture_ids = [
            create_mixture_id(
                components=mixture,
                mixture_key=mixture_key,
                delimiter=delimiter,
                case=case
            ) for mixture in mixtures
        ]

        # store
        res = {
            "mixture_num": len(mixtures),
            "mixture_id": mixture_ids,
        }

        # NOTE: create mixture keys
        if mixture_keys is None:
            mixture_keys = [
                'Name', 'Formula', 'Name-State', 'Formula-State', 'Name-Formula'
            ]

        # iterate through mixtures
        for mixture in mixtures:
            for key in mixture_keys:
                # create mixture id
                mixture_id = create_mixture_id(
                    components=mixture,
                    mixture_key=key,
                    delimiter=delimiter,
                    case=case
                )
                # new key
                key_normalized = "mixture_"+key.strip().replace("-", "_").lower()

                # store
                if key_normalized not in res:
                    res[key_normalized] = []

                res[key_normalized].append(mixture_id)

        # return
        return res
    except Exception as e:
        logger.error(f"Error in generate_mixture_references: {e}")
        return {}


# SECTION: find component by identifier


def find_component_by_id(
        id: str,
        components: List[Component],
        case_sensitive: bool = True,
        mode: Literal['normal', 'strict'] = 'normal'
) -> Optional[Component]:
    """
    Find a component in the list of components by its identifier.

    Parameters
    ----------
    id : str
        The identifier of the component to find.
    components : List[Component]
        The list of components to search.
    case_sensitive : bool, optional
        Whether the search should be case-sensitive. Default is True.
    mode : Literal['normal', 'strict'], optional
        The mode of search. In 'normal' mode, the function will check against multiple identifiers (name-state, formula-state, name-formula, etc.). In 'strict' mode, it will not check Name and Formula.

    Returns
    -------
    Optional[Component]
        The component with the matching identifier, or None if not found.
    """
    # NOTE: normalize input identifier before comparing it with generated IDs.
    component_id = id.strip()

    # NOTE: check if case_sensitive is False, if so convert id to lower case
    if not case_sensitive:
        case = 'lower'
        component_id = component_id.lower()
    else:
        case = None

    # NOTE: iterate through components and check if the id matches any of the component's identifiers
    for component in components:
        # ! check if the id matches any of the component's identifiers
        if (
            set_component_id(component, 'Name-State', case=case) == component_id or
            set_component_id(component, 'Formula-State', case=case) == component_id or
            set_component_id(component, 'Name-Formula', case=case) == component_id or
            set_component_id(component, 'Name-Formula-State', case=case) == component_id or
            set_component_id(
                component,
                'Formula-Name-State',
                case=case
            ) == component_id
        ):
            return component

        # ! for 'Name' and 'Formula' keys, check if the id matches the component's name or formula directly
        if mode == 'normal':
            if (
                set_component_id(
                    component,
                    'Name',
                    case=case
                ) == component_id or
                set_component_id(
                    component,
                    'Formula',
                    case=case
                ) == component_id
            ):
                return component
    return None


def find_components_by_ids(
        ids: List[str],
        components: List[Component],
        case_sensitive: bool = True
) -> Optional[List[Component]]:
    """
    Find multiple components in the list of components by their identifiers.

    Parameters
    ----------
    ids : List[str]
        The list of identifiers of the components to find.
    components : List[Component]
        The list of components to search.
    case_sensitive : bool, optional
        Whether the search should be case-sensitive. Default is True.

    Returns
    -------
    List[Optional[Component]]
        A list of components with the matching identifiers, or None.

    Notes
    -----
    - If `any` of the identifiers do not match any component, the function will return `None`.
    """
    try:
        res: List[Optional[Component]] = [
            find_component_by_id(
                id=id,
                components=components,
                case_sensitive=case_sensitive
            )
            for id in ids
        ]

        # NOTE: any of the results is None, return None
        if any(r is None for r in res):
            return None

        return [r for r in res if r is not None]
    except Exception as e:
        logger.error(f"Error in find_components_by_ids: {e}")
        raise

# ! ::: Configure Component Values by order and component key


def config_components_values(
        values: Dict[str, Any],
        components: List[Component],
        component_key: Optional[ComponentKey],
        case_sensitive: bool = True,
        sort_by_components_order: bool = True,
) -> Optional[Tuple[Dict[str, Any], List[Any]]]:
    """
    Configure values for multiple components based on their identifiers in the component list and an optional component key.

    Parameters
    ----------
    values : Dict[str, float | int]
        A dictionary of component IDs and their corresponding values.
    components : List[Component]
        A list of Component objects.
    component_key : Optional[ComponentKey], optional
        The key to use for identifying components. Defaults to None.
    case_sensitive : bool, optional
        Whether the component IDs are case-sensitive. Defaults to True.
    sort_by_components_order : bool, optional
        Whether to sort the configured values by the order of components in the component list. Defaults to True.

    Returns
    -------
    Optional[Tuple[Dict[str, Any], List[Any]]]
        A tuple containing:
        - A dictionary mapping component identifiers (after applying the component key, if any) to their configured values.
        - A list of the configured values.
        Returns None if the configuration failed.

    Notes
    -----
    - If any identifier does not match any component, it will cause the function to return None.
    """
    # SECTION: validate input
    if not values:
        logger.warning("No values provided")
        return None

    # components
    if not components:
        logger.warning("No components provided")
        return None

    # SECTION: get components values
    # component values
    component_values: Dict[str, Any] = {}

    for comp_id, comp_val in values.items():
        # >>> find component by id
        component_found_ = find_component_by_id(
            id=comp_id,
            components=components,
            case_sensitive=case_sensitive
        )
        # >> check
        if not component_found_:
            logger.warning("Component not found for id: %s", comp_id)
            return None

        # NOTE: find index
        component_index_ = components.index(component_found_)

        # Determine output ID
        output_id = comp_id

        # NOTE: choose a new id
        if component_key:
            output_id = set_component_id(
                component=component_found_,
                component_key=component_key
            )

        if output_id in component_values:
            logger.warning(
                "Duplicate component ID after conversion: %s",
                output_id
            )
            return None

        # update component values with new id
        component_values[output_id] = {
            "value": comp_val,
            "index": component_index_,
        }

    # SECTION: reorder component values
    if sort_by_components_order is True:
        component_values = dict(
            sorted(component_values.items(), key=lambda item: item[1]["index"])
        )

    # NOTE: remove index from component values
    for comp_id in component_values:
        # index
        component_values[comp_id].pop("index", None)
        # value
        component_values[comp_id] = component_values[comp_id]["value"]

    # NOTE: list
    component_values_list = list(component_values.values())

    return component_values, component_values_list
