# import libs
import re
from typing import (
    Literal,
    TypeAlias,
    Any,
    List,
)
from pydantic import (
    BaseModel,
    Field,
    ConfigDict,
    field_validator,
    model_validator,
)
# locals


# SECTION: Component key type
ComponentKey: TypeAlias = Literal[
    'Name-State',
    'Formula-State',
    'Name-Formula',
    'Name',
    'Formula',
    'Name-Formula-State',
    'Formula-Name-State'
]

MixtureKey = ComponentKey

# SECTION: Species type
SpeciesType: TypeAlias = Literal[
    "neutral",
    "cation",
    "anion",
    "radical",
    "zwitterion",
]

# SECTION: Charge centers pattern
_CHARGE_CENTER_PATTERN = re.compile(
    r"\{(?:\*)?(?P<magnitude>\d+)?(?P<sign>[+-])\}"
)

# ! ::: Parsing formula charge


def _parse_charge_centers(formula: str) -> list[int]:
    charges: list[int] = []

    for match in _CHARGE_CENTER_PATTERN.finditer(formula):
        magnitude = match.group("magnitude")
        sign = match.group("sign")

        value = int(magnitude) if magnitude else 1

        if sign == "-":
            value = -value

        charges.append(value)

    return charges


def _parse_formula_charge(formula: str) -> int:
    charges = _parse_charge_centers(formula)
    return sum(charges)

# ! ::: Coerce charge to integer


def _coerce_charge_int(value: Any) -> int:
    if isinstance(value, bool):
        raise ValueError("Charge must be an integer.")

    if isinstance(value, int):
        return value

    if isinstance(value, float):
        if value.is_integer():
            return int(value)
        raise ValueError("Charge must be an integer.")

    if isinstance(value, str):
        value_str = value.strip()
        if re.fullmatch(r"[+-]?\d+", value_str):
            return int(value_str)
        raise ValueError("Charge must be an integer.")

    raise ValueError("Charge must be an integer.")

# ! ::: Parsing species type


def _parse_species_type(formula: str) -> list[SpeciesType]:
    charges = _parse_charge_centers(formula)

    has_positive = any(charge > 0 for charge in charges)
    has_negative = any(charge < 0 for charge in charges)

    # radical detection
    has_radical = bool(
        re.search(r"\{\*(?:\d*[+-])?\}", formula)
    )

    species: list[SpeciesType] = []

    # zwitterion
    if has_positive and has_negative and sum(charges) == 0:
        species.append("zwitterion")

    else:
        net_charge = sum(charges)

        if net_charge > 0:
            species.append("cation")

        elif net_charge < 0:
            species.append("anion")

        else:
            species.append("neutral")

    if has_radical:
        species.append("radical")

    return species


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
    charge : int, optional
        Charge of the component, if applicable. Default is 0.
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
    charge: int = Field(
        default=0,
        description="Charge of the component, if applicable"
    )
    species_type: List[SpeciesType] = Field(
        default_factory=lambda: ["neutral"],
        description="Species classification derived from the chemical formula"
    )
    mole_fraction: float = Field(
        default=0,
        description="Mole fraction of the component in a mixture, if applicable"
    )

    X: dict = Field(
        default_factory=dict,
        description="Custom properties for the component must include 'name', 'value', 'unit', 'symbol"
    )

    # ! ::: Validators for the Component model
    @field_validator("charge", mode="before")
    @classmethod
    def validate_charge(cls, value: Any) -> int:
        return _coerce_charge_int(value)

    # ! ::: Set species type from chemical formula before model validation
    @model_validator(mode="before")
    @classmethod
    def set_species_type_from_formula(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        formula = data.get("formula")

        if not isinstance(formula, str):
            return data

        data = dict(data)
        data["species_type"] = _parse_species_type(formula)

        return data

    # ! ::: Set charge from chemical formula before model validation
    @model_validator(mode="before")
    @classmethod
    def set_charge_from_formula(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        formula = data.get("formula")

        if not isinstance(formula, str):
            return data

        formula_charge = _parse_formula_charge(formula)

        data = dict(data)

        if "charge" not in data or data.get("charge") is None:
            data["charge"] = formula_charge
            return data

        charge = _coerce_charge_int(data["charge"])

        if charge != formula_charge:
            raise ValueError(
                "Component formula charge and charge field are inconsistent: "
                f"formula={formula!r}, charge={data['charge']!r}"
            )

        return data

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
