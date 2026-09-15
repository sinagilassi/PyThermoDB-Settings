from __future__ import annotations

from ..models.quantity import QuantityRef
from ..references.quantities import registry


def quantity_meta(key: str) -> QuantityRef:
    """
    Return resolved metadata for a canonical quantity.

    This is a convenience wrapper around ``registry.ref(key)``.

    Parameters
    ----------
    key : str
        The canonical key of the quantity for which to retrieve metadata.

    Returns
    -------
    QuantityRef
        The resolved metadata for the specified quantity key.
    """
    return registry.ref(key)
