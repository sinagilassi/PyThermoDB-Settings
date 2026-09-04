# import libs
from rich import print
from pythermodb_settings.models import CustomProp, CustomProperty
from pythermodb_settings.utils import get_unit
from pythermodb_settings.utils.tools import UnitData


def print_unit_data(title: str, identifier: str, data: UnitData) -> None:
    print(f"\n{title}")
    print(get_unit(identifier, data))


# A single property always has a consistent unit.
temperature = CustomProp(value=298.15, unit="K")
print_unit_data("Single property", "temperature", temperature)

# Mappings and sequences with one shared unit are consistent.
enthalpies = {
    "water": CustomProperty(
        name="Standard enthalpy of formation",
        description="At 298.15 K",
        value=-285.83,
        unit="kJ/mol",
        symbol="Hf",
    ),
    "ethanol": CustomProp(value=-277.0, unit="kJ/mol"),
}
print_unit_data("Consistent mapping", "enthalpies", enthalpies)

pressures = [
    CustomProp(value=1.0, unit="bar"),
    CustomProp(value=1.2, unit="bar"),
]
print_unit_data("Consistent sequence", "pressures", pressures)

# Different units are reported in all_units and marked inconsistent.
mixed_units = [
    CustomProp(value=1.0, unit="bar"),
    CustomProp(value=101325.0, unit="Pa"),
]
print_unit_data("Inconsistent units", "mixed_pressures", mixed_units)

# Numeric values do not carry units, so mixed and numeric-only inputs
# are both inconsistent.
mixed_values = [CustomProp(value=1.0, unit="mol"), 2.0]
print_unit_data("Mixed properties and numbers", "amounts", mixed_values)
print_unit_data("Numeric-only values", "mole_fractions", [0.25, 0.75])
