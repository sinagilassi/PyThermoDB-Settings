
# import libs
import numpy as np
from typing import Generic, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
)

# NOTE: Generic type variable for AnnotatedValue
T = TypeVar("T")


# SECTION: Annotated Value Model
class AnnotatedValue(BaseModel, Generic[T]):
    """
    Structured representation of a returned value with optional descriptive
    metadata for interpretation by users, applications, and LLM-based agents.

    This model wraps any returned or calculated value together with semantic
    information describing what the value represents. The metadata fields are
    optional so that the model can be used both for simple return values and
    for fully described scientific calculation results.

    The primary purpose of ``AnnotatedValue`` is to make function and tool
    outputs easier for an LLM agent to understand, interpret, explain, and
    reuse. A raw value alone may not provide enough context about its meaning,
    unit, scientific symbol, or calculation basis.

    Only ``value`` is required. All metadata fields are optional.

    Attributes
    ----------
    value : T
        The actual returned or calculated value. The type of this value is specified by the generic type variable ``T``.

    name : str | None
        Optional name identifying the returned quantity or result, e.g.
        ``"enthalpy"``, ``"ionic_strength"``,
        ``"activity_coefficient"``, or ``"converged"``.

    description : str | None
        Optional human-readable explanation of what the returned value
        represents. It may include calculation basis, assumptions, physical
        meaning, or other information useful for interpreting the result.

    unit : str | None
        Optional unit associated with the returned value, e.g.
        ``"kJ/mol"``, ``"mol/kg"``, ``"Pa"``, or ``"dimensionless"``.
        Use ``None`` when a unit does not apply or is not available.

        For scientifically dimensionless quantities, ``"dimensionless"``
        is preferred over ``None`` because it explicitly communicates that
        the quantity has no physical dimension.

    symbol : str | None
        Optional scientific, mathematical, or conventional symbol associated
        with the returned value, e.g. ``"H"`` for enthalpy,
        ``"I"`` for ionic strength, or ``"gamma"`` for an activity
        coefficient.

    aliases : str | None
        Optional description of the aliases details or method used to
        obtain the returned value.

    Notes
    -----
    ``AnnotatedValue`` is intended as a generic agent-facing result wrapper.

    It can be used for:

    - scalar calculation results,
    - vectors, lists, arrays, and matrices,
    - dictionaries and structured calculation outputs,
    - boolean status values,
    - strings or labels,
    - thermodynamic properties,
    - numerical solver results,
    - intermediate calculation results,
    - MCP tool outputs,
    - API responses intended for LLM interpretation.

    When metadata is provided, an LLM agent can determine more reliably:

    - what was calculated,
    - what the returned value represents,
    - which unit applies,
    - which scientific symbol is associated with the result,
    - and how the result should be interpreted or communicated.

    Examples
    --------
    ``AnnotatedValue`` is generic over ``T``, so it can be parameterized with
    the concrete type of ``value`` (e.g. ``AnnotatedValue[int]``,
    ``AnnotatedValue[float]``, ``AnnotatedValue[bool]``,
    ``AnnotatedValue[dict[str, float]]``) for static type checking, or used
    without parameterization when the type is inferred or unimportant.

    A simple value without additional metadata:

    >>> result = AnnotatedValue[int](value=42)

    A boolean result:

    >>> result = AnnotatedValue[bool](
    ...     name="converged",
    ...     value=True,
    ...     description="Indicates whether the numerical solver converged.",
    ... )

    A scientific result:

    >>> result = AnnotatedValue[float](
    ...     name="ionic_strength",
    ...     description="Ionic strength calculated on a molality basis.",
    ...     value=0.125,
    ...     unit="mol/kg",
    ...     symbol="I",
    ... )

    A dimensionless result:

    >>> result = AnnotatedValue[float](
    ...     name="activity_coefficient",
    ...     description="Activity coefficient of the specified component.",
    ...     value=1.21,
    ...     unit="dimensionless",
    ...     symbol="gamma",
    ... )

    A structured result:

    >>> result = AnnotatedValue[dict[str, float]](
    ...     name="component_molalities",
    ...     description="Calculated molality of each dissolved species.",
    ...     value={
    ...         "Na+": 0.1,
    ...         "Cl-": 0.1,
    ...     },
    ...     unit="mol/kg",
    ... )
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow",
        json_encoders={
            np.ndarray: lambda value: value.tolist(),
            np.integer: int,
            np.floating: float,
        },
    )

    value: T = Field(
        ...,
        description=(
            "Actual returned or calculated value. This field is required and "
            "may contain any Python object, including scalar values, strings, "
            "booleans, sequences, mappings, arrays, matrices, or other "
            "structured calculation results."
        ),
    )

    name: str | None = Field(
        default=None,
        description=(
            "Optional name identifying the returned quantity or result, "
            "e.g. 'enthalpy', 'ionic_strength', 'activity_coefficient', "
            "or 'converged'."
        ),
    )

    description: str | None = Field(
        default=None,
        description=(
            "Optional human-readable explanation of what the returned value "
            "represents. May include its physical meaning, calculation basis, "
            "assumptions, conditions, or other context useful to an LLM agent."
        ),
    )

    unit: str | None = Field(
        default=None,
        description=(
            "Optional unit associated with the returned value, e.g. 'kJ/mol', "
            "'mol/kg', 'Pa', or 'dimensionless'. Use None when no unit applies "
            "or unit information is unavailable. Prefer 'dimensionless' for "
            "scientifically dimensionless quantities."
        ),
    )

    symbol: str | None = Field(
        default=None,
        description=(
            "Optional scientific or mathematical symbol associated with the "
            "returned value, e.g. 'H' for enthalpy, 'I' for ionic strength, "
            "or 'gamma' for an activity coefficient."
        ),
    )

    aliases: str | None = Field(
        default=None,
        description=(
            "Optional description of the aliases details or method used "
            "to obtain the returned value."
        ),
    )
