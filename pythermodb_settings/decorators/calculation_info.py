from __future__ import annotations

from typing import Any, Callable, Mapping, ParamSpec, TypeVar, get_type_hints
import inspect

from pydantic import BaseModel, ConfigDict, Field
# locals
from ..models.decorators import CalculationSignature


P = ParamSpec("P")
R = TypeVar("R")

# SECTION: Calculation Info Model


class CalculationInfo(BaseModel):
    """
    Machine-readable metadata describing a scientific calculation.

    The function signature and type hints remain the primary source
    for technical typing information.

    This model provides additional scientific and semantic context
    for humans, agents, MCP servers, and other tooling.

    Attributes
    ----------
    name : str
        Name of the calculation function.
    description : str
        Short description of what the function calculates.
    equation : str | None
        Mathematical equation or defining relationship.
    inputs : dict[str, str]
        Semantic descriptions of important function inputs.
    outputs : dict[str, str]
        Semantic description of the function output.
    aliases : tuple[str, ...]
            Names of equivalent or closely related calculation functions.
    notes : tuple[str, ...]
        Assumptions, limitations, usage conditions, or other scientifically relevant notes.
    """

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    name: str = Field(
        description="Name of the calculation function."
    )

    description: str = Field(
        description="Short description of what the function calculates."
    )

    equation: str | None = Field(
        default=None,
        description="Mathematical equation or defining relationship.",
    )

    inputs: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Semantic descriptions of important function inputs. "
            "Keys should normally match function parameter names."
        ),
    )

    outputs: dict[str, str] = Field(
        default_factory=dict,
        description=(
            "Semantic description of the function outputs. "
            "Keys should normally match function return value names."
        ),
    )

    aliases: tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "Names of equivalent or closely related calculation functions."
        ),
    )

    notes: tuple[str, ...] = Field(
        default_factory=tuple,
        description=(
            "Assumptions, limitations, usage conditions, or other "
            "scientifically relevant notes."
        ),
    )

# SECTION Calculation Info Decorator


def calculation_info(
    *,
    name: str,
    description: str,
    equation: str | None = None,
    inputs: Mapping[str, str] | None = None,
    outputs: Mapping[str, str] | None = None,
    notes: tuple[str, ...] = (),
    aliases: tuple[str, ...] = (),
) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Attach machine-readable calculation metadata to a function.

    The computational behavior of the decorated function is unchanged.

    Metadata is available through::

        func.__calculation_info__

    Parameters
    ----------
    name:
        Name of the calculation function.

    description:
        Short scientific description of the calculation.

    equation:
        Mathematical equation or defining relationship.

    inputs:
        Mapping of function argument names to their semantic descriptions.

    outputs:
        Mapping of return-value names to their semantic descriptions.

    aliases:
        Names of equivalent or closely related calculation functions.

    notes:
        Assumptions, limitations, applicability conditions, or other
        relevant scientific information.

    Returns
    -------
    Callable
        Decorated function containing ``__calculation_info__`` metadata.
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        info = CalculationInfo(
            name=name,
            description=description,
            equation=equation,
            inputs=dict(inputs) if inputs is not None else {},
            outputs=dict(outputs) if outputs is not None else {},
            aliases=aliases,
            notes=notes,
        )

        func.__calculation_info__ = info  # type: ignore[attr-defined]

        return func

    return decorator

# ! ::: Calculation Signature Retrieval


def get_calculation_info(
    func: Callable[..., Any],
) -> CalculationInfo | None:
    """
    Return calculation metadata attached to a function.

    Returns
    -------
    CalculationInfo | None
        Calculation metadata if available, otherwise None.
    """

    return getattr(func, "__calculation_info__", None)

# ! ::: Calculation Signature Retrieval


def get_calculation_signature(
    func: Callable[..., Any],
) -> CalculationSignature:

    hints = get_type_hints(
        func,
        include_extras=True,
    )

    signature = inspect.signature(func)

    parameters = {
        name: hints.get(name, parameter.annotation)
        for name, parameter in signature.parameters.items()
    }

    return CalculationSignature(
        parameters=parameters,
        return_type=hints.get(
            "return",
            signature.return_annotation,
        ),
    )
