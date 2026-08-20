# import libs
from typing import (
    Literal,
    TypeAlias
)
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    model_validator
)
# locals

# SECTION: Component key type
ComponentKey = Literal[
    'Name-State',
    'Formula-State',
    'Name-Formula',
    'Name',
    'Formula',
    'Name-Formula-State',
    'Formula-Name-State'
]

MixtureKey = ComponentKey

# SECTION: Component model


class Component(BaseModel):
    """
    Component model for input validation

    Attributes
    ----------
    name : str
        Name of the component.
    formula : str
        Chemical formula of the component.
    state : Literal['g', 'l', 's', 'aq']
        State of the component: 'g' for gas, 'l' for liquid, 's' for solid, 'aq' for aqueous.
    mole_fraction : float, optional
        Mole fraction of the component in a mixture, if applicable. Default is 1.0.
    X: dict, optional
        Custom properties for the component. Must include 'name', 'value', 'unit', and 'symbol'. Default is an empty dictionary.
    """
    name: str = Field(..., description="Name of the component")
    formula: str = Field(..., description="Chemical formula of the component")
    state: Literal['g', 'l', 's', 'aq'] = Field(
        ...,
        description="State of the component: 'g' for gas, 'l' for liquid, 's' for solid, 'aq' for aqueous"
    )
    mole_fraction: float = Field(
        default=0,
        description="Mole fraction of the component in a mixture, if applicable"
    )

    X: dict = Field(
        default_factory=dict,
        description="Custom properties for the component must include 'name', 'value', 'unit', 'symbol"
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow"
    )


# SECTION: Component identity model
class ComponentIdentity(BaseModel):
    """
    Model for component identity.

    Attributes
    ----------
    name_state : str
        Component name-state identifier.
    formula_state : str
        Component formula-state identifier.
    name_formula : str
        Component name-formula identifier.
    """
    name_state: str = Field(
        ...,
        description="Component name-state identifier"
    )
    formula_state: str = Field(
        ...,
        description="Component formula-state identifier"
    )
    name_formula: str = Field(
        ...,
        description="Component name-formula identifier"
    )


# SECTION: Mixture model
Mixture: TypeAlias = list[Component]

# SECTION: Mixture identity model


class MixtureIdentity(BaseModel):
    """
    Model for mixture identity.

    Attributes
    ----------
    name_state : str
        Mixture name-state identifier, e.g., "water-l|ethanol-l".
    formula_state : str
        Mixture formula-state identifier, e.g., "H2O-l|C2H6O-l".
    name_formula : str
        Mixture name-formula identifier, e.g., "water-H2O|ethanol-C2H6O".
    """
    name_state: str = Field(
        ...,
        description="Mixture name-state identifier"
    )
    formula_state: str = Field(
        ...,
        description="Mixture formula-state identifier"
    )
    name_formula: str = Field(
        ...,
        description="Mixture name-formula identifier"
    )


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


class ComponentComposition(BaseModel):
    """
    Composition information for a single component in a mixture.

    The ``amount`` field is interpreted according to the composition basis
    defined by the parent :class:`MixtureComposition` model. It may therefore
    represent an absolute amount, fraction, concentration, molality, or
    partial pressure.

    Attributes
    ----------
    component : Component
        Component associated with the composition value.
    amount : float
        Composition value of the component according to the selected
        composition basis. Must be non-negative.
    """

    component: Component = Field(
        ...,
        description="Component associated with the composition value",
    )

    amount: float = Field(
        ...,
        ge=0,
        description="Component composition value according to the selected basis",
    )
    unit: str = Field(
        ...,
        description="Unit associated with the component composition value",
    )


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
    components : list[ComponentComposition]
        Component composition entries defining the multi-component mixture.
    reference : CompositionReference, optional
        Optional reference quantity associated with the selected composition
        basis. Default is ``None``.
    """

    basis: CompositionBasis = Field(
        ...,
        description="Basis used to express the mixture composition",
    )

    components: list[ComponentComposition] = Field(
        ...,
        description="Composition entries for the components in the mixture",
    )

    reference: CompositionReference | None = Field(
        default=None,
        description="Optional reference quantity associated with the composition basis",
    )

    @model_validator(mode="after")
    def set_component_composition_properties(self):
        """
        Set the composition property in each component's ``X`` dictionary.

        The property metadata is determined from the selected composition
        basis and the component composition amount.

        Returns
        -------
        MixtureComposition
            Validated mixture composition with updated component properties.
        """
        # NOTE: retrieve metadata for the selected basis
        metadata = COMPOSITION_METADATA.get(self.basis)
        # >> check
        if metadata is None:
            raise ValueError(
                f"Invalid composition basis: {self.basis}. Must be one of {list(COMPOSITION_METADATA.keys())}"
            )

        for component_composition in self.components:
            component_composition.component.X['composition'] = {
                "name": metadata["name"],
                "value": component_composition.amount,
                "unit": component_composition.unit,
            }

        return self
