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
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="allow"
    )

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

    def has_species_type(self, species_type: SpeciesType) -> bool:
        """Return whether the component has the given species classification."""
        return species_type in self.species_type

    # ! check neutrality
    def is_neutral(self) -> bool:
        return self.has_species_type("neutral")

    # ! check cation
    def is_cation(self) -> bool:
        return self.has_species_type("cation")

    # ! check anion
    def is_anion(self) -> bool:
        return self.has_species_type("anion")

    # ! check radical
    def is_radical(self) -> bool:
        return self.has_species_type("radical")

    # ! check zwitterion
    def is_zwitterion(self) -> bool:
        return self.has_species_type("zwitterion")

    # ! check ionic
    def is_ionic(self) -> bool:
        """
        Return True if the species has ionic character.

        Includes:
        - cations
        - anions
        - zwitterions
        """
        return (
            self.is_cation()
            or self.is_anion()
            or self.is_zwitterion()
        )

    # ! ::: Charge helpers

    def get_charge_centers(self) -> list[int]:
        """
        Return all explicit local charge centers encoded in the formula.

        Examples
        --------
        Na{+}                  -> [1]
        SO4{2-}                -> [-2]
        NH3{+}-CH2-COO{-}      -> [1, -1]
        """
        return _parse_charge_centers(self.formula)

    def get_net_charge(self) -> int:
        """
        Return the net charge of the component.
        """
        return self.charge

    def has_charge_centers(self) -> bool:
        """
        Return True if the formula contains one or more explicit charge centers.
        """
        return bool(self.get_charge_centers())

    def has_internal_charges(self) -> bool:
        """
        Return True if the species contains explicit local charge centers.

        This is especially useful for zwitterions, whose net charge is zero
        but which contain positive and negative charge centers.
        """
        return self.has_charge_centers()

    def get_charge_center_count(self) -> int:
        """
        Return the total number of explicit charge centers.
        """
        return len(self.get_charge_centers())

    def get_positive_charge_count(self) -> int:
        """
        Return the number of positive charge centers.
        """
        return sum(
            charge > 0
            for charge in self.get_charge_centers()
        )

    def get_negative_charge_count(self) -> int:
        """
        Return the number of negative charge centers.
        """
        return sum(
            charge < 0
            for charge in self.get_charge_centers()
        )

    def get_total_positive_charge(self) -> int:
        """
        Return the sum of all positive local charges.

        Example
        -------
        X{2+}-Y{+} -> 3
        """
        return sum(
            charge
            for charge in self.get_charge_centers()
            if charge > 0
        )

    def get_total_negative_charge(self) -> int:
        """
        Return the sum of all negative local charges.

        Example
        -------
        X{2-}-Y{-} -> -3
        """
        return sum(
            charge
            for charge in self.get_charge_centers()
            if charge < 0
        )

    def is_charged(self) -> bool:
        """
        Return True if the component has a non-zero net charge.
        """
        return self.charge != 0

    # ! ::: Radical helpers

    def get_radical_count(self) -> int:
        """
        Return the number of radical annotations in the formula.

        Examples
        --------
        OH{*}       -> 1
        O2{*-}      -> 1
        """
        return len(
            re.findall(
                r"\{\*(?:\d*[+-])?\}",
                self.formula
            )
        )

    def has_radical_centers(self) -> bool:
        """
        Return True if the formula contains at least one radical marker.
        """
        return self.get_radical_count() > 0

    def is_radical_ion(self) -> bool:
        """
        Return True if the component is both radical and electrically charged.
        """
        return self.is_radical() and self.is_charged()

    # ! ::: Phase helpers

    def is_gas(self) -> bool:
        """
        Return True if the component is in the gas phase.
        """
        return self.state == "g"

    def is_liquid(self) -> bool:
        """
        Return True if the component is in the liquid phase.
        """
        return self.state == "l"

    def is_solid(self) -> bool:
        """
        Return True if the component is in the solid phase.
        """
        return self.state == "s"

    def is_aqueous(self) -> bool:
        """
        Return True if the component is in the aqueous phase.
        """
        return self.state == "aq"

    # ! ::: Formula helpers

    def get_base_formula(self) -> str:
        """
        Return the formula with charge and radical annotations removed.

        Examples
        --------
        Na{+}                  -> Na
        SO4{2-}                -> SO4
        OH{*}                  -> OH
        O2{*-}                 -> O2
        NH3{+}-CH2-COO{-}      -> NH3-CH2-COO
        """

        formula = self.formula

        # remove charged radical annotations such as {*+}, {*-}, {*2+}
        formula = re.sub(
            r"\{\*\d*[+-]\}",
            "",
            formula
        )

        # remove pure radical annotation {*}
        formula = re.sub(
            r"\{\*\}",
            "",
            formula
        )

        # remove charge annotations such as {+}, {-}, {2+}, {3-}
        formula = re.sub(
            r"\{\d*[+-]\}",
            "",
            formula
        )

        return formula

    def has_annotations(self) -> bool:
        """
        Return True if the formula contains charge or radical annotations.
        """
        return bool(
            re.search(
                r"\{[^{}]+\}",
                self.formula
            )
        )

    # ! ::: Identity helpers

    def get_name_state(self) -> str:
        """
        Return the Name-State identifier.

        Example
        -------
        sulfate + aq -> sulfate-aq
        """
        return f"{self.name}-{self.state}"

    def get_formula_state(self) -> str:
        """
        Return the Formula-State identifier.

        Example
        -------
        SO4{2-} + aq -> SO4{2-}-aq
        """
        return f"{self.formula}-{self.state}"

    def get_name_formula(self) -> str:
        """
        Return the Name-Formula identifier.

        Example
        -------
        sulfate + SO4{2-} -> sulfate-SO4{2-}
        """
        return f"{self.name}-{self.formula}"

    def get_name_formula_state(self) -> str:
        """
        Return the Name-Formula-State identifier.
        """
        return f"{self.name}-{self.formula}-{self.state}"

    def get_formula_name_state(self) -> str:
        """
        Return the Formula-Name-State identifier.
        """
        return f"{self.formula}-{self.name}-{self.state}"

    def get_key(self, key: ComponentKey) -> str:
        """
        Build a component identifier according to the requested key format.
        """

        mapping = {
            "Name-State": self.get_name_state,
            "Formula-State": self.get_formula_state,
            "Name-Formula": self.get_name_formula,
            "Name": lambda: self.name,
            "Formula": lambda: self.formula,
            "Name-Formula-State": self.get_name_formula_state,
            "Formula-Name-State": self.get_formula_name_state,
        }

        return mapping[key]()

    def get_identity(self) -> "ComponentIdentity":
        """
        Build and return the ComponentIdentity representation.
        """
        return ComponentIdentity(
            name_state=self.get_name_state(),
            formula_state=self.get_formula_state(),
            name_formula=self.get_name_formula(),
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
