from __future__ import annotations

import inspect
from functools import wraps
from typing import Callable, ParamSpec, TypeVar
# locals
from pythermodb_settings.models.agents import AnnotatedValue

# SECTION: Type Variables
P = ParamSpec("P")
T = TypeVar("T")

# SECTION: Decorator Definition


def annotated_value(
    func: Callable[P, T],
) -> Callable[P, AnnotatedValue[T]]:
    """
    Decorator to wrap the return value of a function in an AnnotatedValue.

    The decorated function should have optional keyword arguments for
    name, description, unit, and symbol, which will be used to populate
    the corresponding fields in the AnnotatedValue.

    Parameters
    ----------
    func : Callable[P, T]
        The function to be decorated. P represents the parameter specification for the function's arguments whereas T represents the return type of the function.

    Returns
    -------
    Callable[P, AnnotatedValue[T]]
        A new function that returns an AnnotatedValue wrapping the original result.
    """

    signature = inspect.signature(func)

    @wraps(func)
    def wrapper(
        *args: P.args,
        **kwargs: P.kwargs,
    ) -> AnnotatedValue[T]:

        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()

        result = func(*args, **kwargs)

        return AnnotatedValue[T](
            value=result,
            name=bound.arguments.get("name"),
            description=bound.arguments.get("description"),
            unit=bound.arguments.get("unit"),
            symbol=bound.arguments.get("symbol"),
            aliases=bound.arguments.get("aliases"),
        )

    return wrapper
