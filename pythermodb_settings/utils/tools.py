# import libs
import time
import logging
from functools import wraps
from typing import Literal
from collections.abc import Mapping, Sequence
from typing import Any, TypedDict

from ..models import CustomProperty, CustomProp, AnnotatedValue

# NOTE: logger setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ModeType = Literal["silent", "log", "attach"]

# ! ::: Measure Time


def measure_time(func):
    '''
    Decorator to measure the execution time of a function.

    Parameters
    ----------
    func : Callable
        The function to be decorated.

    Returns
    -------
    Callable
        The wrapped function with time measurement.

    Notes
    -----
    - The decorator adds a 'mode' keyword argument to the decorated function.
    - 'mode' can be 'silent', 'log', or 'attach':
        - 'silent': No logging or attachment of time.
        - 'log': Logs the execution time.
        - 'attach': Logs and attaches the execution time to the result.
    - default mode is 'silent'.
    '''
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Extract mode safely
        mode: ModeType = kwargs.pop("mode", "silent")

        start = time.process_time()
        result = func(*args, **kwargs)
        end = time.process_time()

        elapsed = end - start

        if mode == "silent":
            return result

        if mode == "log":
            logger.info(
                f"{func.__name__} executed in {elapsed:.6f} seconds (CPU time)")
            return result

        if mode == "attach":
            logger.info(
                f"{func.__name__} executed in {elapsed:.6f} seconds (CPU time)")
            if isinstance(result, dict):
                result["computation_time"] = elapsed
            else:
                result = {
                    "result": result,
                    "computation_time": elapsed
                }
            return result

        raise ValueError("mode must be 'silent', 'log', or 'attach'")
    return wrapper


# ! ::: Create Annotated Value


def to_annotated_value(
    value: Any,
    name: str | None = None,
    description: str | None = None,
    unit: str | None = None,
    symbol: str | None = None,
) -> AnnotatedValue:
    """
    Create an AnnotatedValue instance with the given attributes.

    Parameters
    ----------
    value : Any
        The actual returned or calculated value.
    name : str | None, optional
        Optional name identifying the returned quantity or result.
    description : str | None, optional
        Optional human-readable explanation of what the returned value represents.
    unit : str | None, optional
        Optional unit associated with the returned value.
    symbol : str | None, optional
        Optional scientific or mathematical symbol associated with the returned value.

    Returns
    -------
    AnnotatedValue
        The created AnnotatedValue instance.
    """
    return AnnotatedValue(
        value=value,
        name=name,
        description=description,
        unit=unit,
        symbol=symbol,
    )


# ! Get Unit

# SECTION: Types


class PropertyDict(TypedDict):
    """
    Dictionary representation of a property.

    Attributes
    ----------
    value : float | int
        Numerical value of the property.
    unit : str
        Unit associated with the property.
    """

    value: float | int
    unit: str


UnitValue = (
    float
    | int
    | CustomProp
    | CustomProperty
    | PropertyDict
)


UnitData = (
    Mapping[str, UnitValue]
    | Sequence[UnitValue]
    | CustomProp
    | CustomProperty
    | PropertyDict
)


# ! Internal Unit Extractor


def _extract_unit(
    value: (
        float
        | int
        | CustomProp
        | CustomProperty
        | Mapping[str, Any]
    ),
) -> str | None:
    """
    Extract a unit from a supported value.

    Parameters
    ----------
    value : float | int | CustomProp | CustomProperty | Mapping[str, Any]
        Value from which unit information should be extracted.

    Returns
    -------
    str | None
        Unit if available, otherwise None.
    """

    # Custom property models
    if isinstance(value, (CustomProp, CustomProperty)):
        return value.unit

    # Dictionary-like property
    if isinstance(value, Mapping):
        unit = value.get("unit")

        if isinstance(unit, str):
            return unit

    # Raw numerical value
    return None


# ! Get Unit


def get_unit(
    identifier: str,
    data: UnitData,
) -> dict[str, Any]:
    """
    Get unit information from the given data.

    The input can be:

    - CustomProp
    - CustomProperty
    - property dictionary containing ``value`` and ``unit``
    - Mapping of properties
    - Sequence of properties
    - numeric values

    For mappings and sequences, all elements must contain unit information
    and all units must be identical for the collection to be considered
    consistent.

    Raw numerical values do not carry unit information.

    Parameters
    ----------
    identifier : str
        Identifier associated with the supplied data.
    data : UnitData
        Property or collection from which unit information is extracted.

    Returns
    -------
    dict[str, Any]
        Dictionary containing:

        ``id``
            Identifier associated with the input data.

        ``unit``
            Common unit when all elements contain the same unit,
            otherwise None.

        ``consistent``
            True when valid and identical unit information exists for
            all elements.

        ``all_units``
            List of units discovered in the supplied data.

    Examples
    --------
    Single CustomProp:

    >>> get_unit(
    ...     "amount",
    ...     CustomProp(value=10.0, unit="mol"),
    ... )
    {
        "id": "amount",
        "unit": "mol",
        "consistent": True,
        "all_units": ["mol"],
    }

    Property dictionary:

    >>> get_unit(
    ...     "amount",
    ...     {
    ...         "value": 10.0,
    ...         "unit": "mol",
    ...     },
    ... )

    Mapping of properties:

    >>> get_unit(
    ...     "component_moles",
    ...     {
    ...         "H2O": CustomProp(value=2.0, unit="mol"),
    ...         "CO2": {"value": 1.0, "unit": "mol"},
    ...     },
    ... )

    Mixed unit and raw numeric values are considered inconsistent:

    >>> get_unit(
    ...     "component_moles",
    ...     {
    ...         "H2O": CustomProp(value=2.0, unit="mol"),
    ...         "CO2": 1.0,
    ...     },
    ... )
    """

    # NOTE: single CustomProp / CustomProperty
    if isinstance(data, (CustomProp, CustomProperty)):
        return {
            "id": identifier,
            "unit": data.unit,
            "consistent": True,
            "all_units": [data.unit],
        }

    # NOTE: single property dictionary
    #
    # Example:
    # {
    #     "value": 10.0,
    #     "unit": "mol",
    # }
    if (
        isinstance(data, Mapping)
        and "value" in data
        and "unit" in data
    ):
        unit = _extract_unit(data)

        return {
            "id": identifier,
            "unit": unit,
            "consistent": unit is not None,
            "all_units": [unit] if unit is not None else [],
        }

    # NOTE: mapping collection
    #
    # Example:
    # {
    #     "H2O": CustomProp(...),
    #     "CO2": CustomProp(...),
    # }
    if isinstance(data, Mapping):
        values = list(data.values())

    # NOTE: sequence collection
    #
    # Example:
    # [
    #     CustomProp(...),
    #     CustomProp(...),
    # ]
    elif isinstance(data, Sequence) and not isinstance(
        data,
        (str, bytes),
    ):
        values = list(data)

    # NOTE: unsupported / raw scalar
    else:
        return {
            "id": identifier,
            "unit": None,
            "consistent": False,
            "all_units": [],
        }

    # NOTE: empty collection
    if not values:
        return {
            "id": identifier,
            "unit": None,
            "consistent": False,
            "all_units": [],
        }

    # NOTE: extract unit from every element
    units = [
        _extract_unit(value)
        for value in values
    ]

    # NOTE: preserve only discovered units
    available_units = [
        unit
        for unit in units
        if unit is not None
    ]

    # NOTE: no element contains unit information
    if not available_units:
        return {
            "id": identifier,
            "unit": None,
            "consistent": False,
            "all_units": [],
        }

    # NOTE:
    # Some elements contain units while others do not.
    #
    # Example:
    # {
    #     "H2O": CustomProp(value=2, unit="mol"),
    #     "CO2": 1.0,
    # }
    #
    # We should NOT assume that CO2 is also in mol.
    if len(available_units) != len(values):
        return {
            "id": identifier,
            "unit": None,
            "consistent": False,
            "all_units": available_units,
        }

    # NOTE: all elements have unit information
    consistent = len(set(available_units)) == 1

    return {
        "id": identifier,
        "unit": (
            available_units[0]
            if consistent
            else None
        ),
        "consistent": consistent,
        "all_units": available_units,
    }
