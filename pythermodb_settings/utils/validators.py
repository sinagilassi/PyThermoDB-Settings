# import libs
import logging
from collections.abc import Mapping
# locals
from ..models.quantities import ComponentValues
from .quantity import to_dict, to_list

# NOTE: logger
logger = logging.getLogger(__name__)

# SECTION: Component Value Validators
# ! ::: Check non empty component collections


def non_empty(
        values: ComponentValues,
        name: str
) -> None:
    """
    Validate that a component collection is not empty.

    Parameters
    ----------
    values : ComponentValues
        A component value mapping or sequence to validate.
    name : str
        The name of the collection used in the error message.

    Raises
    ------
    ValueError
        If `values` contains no components.
    """
    if len(values) == 0:
        raise ValueError(f"{name} cannot be empty.")

# ! :::Check non-negative component values


def non_negative(
        values: ComponentValues,
        name: str
) -> None:
    """
    Validate that all component values are non-negative.

    Parameters
    ----------
    values : ComponentValues
        A component value mapping or sequence to validate.
    name : str
        The name of the values used in the error message.

    Raises
    ------
    ValueError
        If any component value is negative.
    """
    items = to_dict(values).values() if isinstance(
        values, Mapping) else to_list(values)
    if any(value < 0.0 for value in items):
        raise ValueError(f"{name} cannot contain negative values.")

# ! :::Check positive component values


def positive(values: ComponentValues, name: str) -> None:
    """
    Validate that all component values are greater than zero.

    Parameters
    ----------
    values : ComponentValues
        A component value mapping or sequence to validate.
    name : str
        The name of the values used in the error message.

    Raises
    ------
    ValueError
        If any component value is zero or negative.
    """
    items = to_dict(values).values() if isinstance(
        values, Mapping) else to_list(values)
    if any(value <= 0.0 for value in items):
        raise ValueError(f"{name} values must be greater than zero.")

# ! :::Check fraction-like component values


def fractions(
        values: ComponentValues,
        name: str,
) -> None:
    """
    Validate fraction-like values on the closed interval [0, 1].

    Parameters
    ----------
    values : ComponentValues
        A component value mapping or sequence to validate.
    name : str
        The name of the values used in the error message.

    Raises
    ------
    ValueError
        If `values` is empty, contains a negative value, or contains a value
        greater than one.
    """
    non_empty(values, name)
    non_negative(values, name)

    # NOTE: Normalization is not enforced here because these functions normalize
    # the converted basis from the supplied component values.
    items = to_dict(values).values() if isinstance(
        values, Mapping) else to_list(values)
    if any(value > 1.0 for value in items):
        raise ValueError(f"{name} cannot contain values greater than one.")
