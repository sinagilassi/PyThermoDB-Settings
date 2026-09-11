# import

from typing import Any
from ..models import CustomProp

# SECTION: Value Extraction


def extract_values(
        value: Any,
) -> float | None:
    """
    Extract the underlying value from a given input, handling various types such as CustomProp, objects with a 'value' attribute, and dictionaries with a 'value' key.

    Parameters
    ----------
    value : Any
        The input value to extract from.

    Returns
    -------
    float | None
        The extracted value, or None if it cannot be extracted.

    Notes
    -----
    - If the input is a CustomProp, its 'value' attribute is returned.
    - If the input has a 'value' attribute, that attribute is returned.
    - If the input is a dictionary with a 'value' key, the corresponding value is returned.
    - If the input is a numeric type (float or int), it is returned as-is.
    - For all other types, the input is returned unchanged.
    """
    # NOTE:
    if isinstance(value, CustomProp):
        # ? CustomProp
        return float(value.value)
    elif getattr(value, "value", None) is not None:
        # ? Object with a 'value' attribute
        return float(value.value)
    elif isinstance(value, dict) and "value" in value:
        # ? Dictionary with a 'value' key
        return float(value["value"])
    elif isinstance(value, (float, int)):
        # ? Numeric types
        return float(value)
    else:
        return None
