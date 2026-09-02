# import libs
from typing import (
    Literal,
    TypeAlias,
    Dict,
    List
)
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    model_validator
)
# locals
from .conditions import CustomProp
from .components import Component

# SECTION: Composition Configuration Model
# NOTE: composition metadata for different bases
COMPOSITION_METADATA = {
    "moles": {
        "name": "moles",
        "symbol": "n",
    },
    "mass": {
        "name": "mass",
        "symbol": "m",
    },
    "volume": {
        "name": "volume",
        "symbol": "V",
    },
    "mole_fraction": {
        "name": "mole_fraction",
        "symbol": "x",
    },
    "mass_fraction": {
        "name": "mass_fraction",
        "symbol": "w",
    },
    "volume_fraction": {
        "name": "volume_fraction",
        "symbol": "phi",
    },
    "molar_concentration": {
        "name": "molar_concentration",
        "symbol": "c",
    },
    "mass_concentration": {
        "name": "mass_concentration",
        "symbol": "rho",
    },
    "molality": {
        "name": "molality",
        "symbol": "b",
    },
    "partial_pressure": {
        "name": "partial_pressure",
        "symbol": "p",
    },
}

AmountBasis: TypeAlias = Literal[
    "moles",
    "mass",
    "volume",
]

FractionBasis: TypeAlias = Literal[
    "mole_fraction",
    "mass_fraction",
    "volume_fraction",
]

ConcentrationBasis: TypeAlias = Literal[
    "molar_concentration",
    "mass_concentration",
    "molality",
]

GasCompositionBasis: TypeAlias = Literal[
    "partial_pressure",
]

CompositionBasis: TypeAlias = (
    AmountBasis
    | FractionBasis
    | ConcentrationBasis
    | GasCompositionBasis
)


class CompositionReference(BaseModel):
    """
    Reference quantity associated with a mixture composition.

    This model defines an optional reference quantity used to convert a
    composition expressed on a relative or intensive basis into component
    amounts or other extensive quantities.

    The physical meaning of the reference depends on the selected
    composition basis. For example, it may represent total moles for a
    mole-fraction basis, total mass for a mass-fraction basis, solution
    volume for a concentration basis, or total pressure for a
    partial-pressure basis.

    Attributes
    ----------
    value : float
        Numerical value of the reference quantity. Must be non-negative.
    unit : str
        Unit associated with the reference quantity, e.g. ``"mol"``,
        ``"kg"``, ``"m3"``, ``"L"``, or ``"bar"``.
    """

    value: float = Field(
        ...,
        ge=0,
        description="Numerical value of the composition reference quantity",
    )

    unit: str = Field(
        ...,
        description="Unit associated with the composition reference quantity",
    )


ComponentComposition: TypeAlias = Dict[str, CustomProp]


class MixtureComposition(BaseModel):
    """
    Composition model for a multi-component mixture.

    This model describes the composition of a mixture using a selected
    composition basis. Supported bases include absolute amounts, fractions,
    concentrations, molality, and partial pressure.

    An optional :class:`CompositionReference` can be supplied when additional
    information is required to convert the specified composition into
    absolute component quantities.

    Examples of reference quantities include:

    - total moles for ``"mole_fraction"``
    - total mass for ``"mass_fraction"``
    - total volume for ``"volume_fraction"``
    - solution volume for ``"molar_concentration"`` or
    ``"mass_concentration"``
    - solvent mass for ``"molality"``
    - total pressure for ``"partial_pressure"``

    Attributes
    ----------
    basis : CompositionBasis
        Basis used to express the mixture composition.
    components : ComponentComposition
        Component composition entries defining the multi-component mixture.
    reference : CompositionReference, optional
        Optional reference quantity associated with the selected composition
        basis. Default is ``None``.
    """

    basis: CompositionBasis = Field(
        ...,
        description="Basis used to express the mixture composition",
    )

    components: List[Component] = Field(
        ...,
        description="List of components in the mixture",
    )

    compositions: ComponentComposition = Field(
        ...,
        description="Composition entries for the components in the mixture",
    )

    reference: CompositionReference | None = Field(
        default=None,
        description="Optional reference quantity associated with the composition basis",
    )


# SECTION: Mixture Composition Models
# NOTE: mole fraction
MixtureMoleFraction: TypeAlias = Dict[str, float]

# NOTE: mass fraction
MixtureMassFraction: TypeAlias = Dict[str, float]

# NOTE: volume fraction
MixtureVolumeFraction: TypeAlias = Dict[str, float]

# NOTE: mole concentration
MixtureMolarConcentration: TypeAlias = Dict[str, float]

# NOTE: mass concentration
MixtureMassConcentration: TypeAlias = Dict[str, float]

# NOTE: molality
MixtureMolality: TypeAlias = Dict[str, float]

# NOTE: partial pressure
MixturePartialPressure: TypeAlias = Dict[str, float]

# NOTE: mole
MixtureMoles: TypeAlias = Dict[str, float]

# NOTE: mass
MixtureMass: TypeAlias = Dict[str, float]

# NOTE: volume
MixtureVolume: TypeAlias = Dict[str, float]
