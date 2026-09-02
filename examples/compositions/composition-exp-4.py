# import libs
import sys
from pathlib import Path

from rich import print

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from pycuc import convert_from_to
from pythermodb_settings.models import Component, CustomProp
from pythermodb_settings.utils import to_amounts, to_amounts_by_order


# =======================================
# create components
# =======================================
# NOTE: define components in the canonical order expected by a calculation
CO2 = Component(
    name="carbon dioxide",
    formula="CO2",
    state="g",
)
H2 = Component(
    name="hydrogen",
    formula="H2",
    state="g",
)
CH3OH = Component(
    name="methanol",
    formula="CH3OH",
    state="g",
)
H2O = Component(
    name="water",
    formula="H2O",
    state="g",
)

components = [CO2, H2, CH3OH, H2O]


# =======================================
# to_amounts
# =======================================
# NOTE: numeric values are cast to float
numeric_amounts = {
    "carbon dioxide": 1,
    "hydrogen": 3.0,
    "methanol": 0,
    "water": 0.5,
}

amounts = to_amounts(numeric_amounts)
print("[bold green]numeric amounts[/bold green]")
print(amounts)


# NOTE: CustomProp values are converted to their numeric value
custom_prop_amounts = {
    "carbon dioxide": CustomProp(value=1.0, unit="g"),
    "hydrogen": CustomProp(value=3.0, unit="g"),
    "methanol": CustomProp(value=0.25, unit="g"),
    "water": CustomProp(value=0.75, unit="g"),
}

amounts = to_amounts(
    component_amounts=custom_prop_amounts,
    output_unit="kg",
    unit_conversion_fn=convert_from_to,
)
print("[bold green]CustomProp amounts converted to kg[/bold green]")
print(amounts)


# =======================================
# to_amounts_by_order
# =======================================
# NOTE: input order can differ from the component order
unordered_amounts = {
    "water": CustomProp(value=0.75, unit="g"),
    "hydrogen": CustomProp(value=3.0, unit="g"),
    "carbon dioxide": CustomProp(value=1.0, unit="g"),
    "methanol": CustomProp(value=0.25, unit="g"),
}

ordered_by_name = to_amounts_by_order(
    component_amounts=unordered_amounts,
    components=components,
    component_key="Name",
    output_unit="g",
)
print("[bold blue]ordered by components list with Name keys[/bold blue]")
print(ordered_by_name)


# NOTE: component_key can normalize the output identifiers
formula_state_amounts = {
    "H2O-g": CustomProp(value=0.75, unit="g"),
    "H2-g": CustomProp(value=3.0, unit="g"),
    "CO2-g": CustomProp(value=1.0, unit="g"),
    "CH3OH-g": CustomProp(value=0.25, unit="g"),
}

ordered_by_formula_state = to_amounts_by_order(
    component_amounts=formula_state_amounts,
    components=components,
    component_key="Formula-State",
    output_unit="kg",
    unit_conversion_fn=convert_from_to,
)
print("[bold blue]ordered with Formula-State keys[/bold blue]")
print(ordered_by_formula_state)


# NOTE: case-insensitive lookup is available for user-supplied identifiers
case_insensitive_amounts = {
    "Water-G": 0.75,
    "Hydrogen-G": 3.0,
    "Carbon Dioxide-G": 1.0,
    "Methanol-G": 0.25,
}

ordered_case_insensitive = to_amounts_by_order(
    component_amounts=case_insensitive_amounts,
    components=components,
    component_key="Name-State",
    case_sensitive=False,
)
print("[bold blue]ordered with case-insensitive matching[/bold blue]")
print(ordered_case_insensitive)


# NOTE: disable sorting when preserving input order is needed
preserved_input_order = to_amounts_by_order(
    component_amounts=unordered_amounts,
    components=components,
    component_key="Name",
    sort_by_components_order=False,
    output_unit="g",
)
print("[bold blue]preserved input order[/bold blue]")
print(preserved_input_order)


# NOTE: returns None if any amount key cannot be matched to a component
missing_component_amounts = {
    "carbon dioxide": 1.0,
    "nitrogen": 2.0,
}

missing_component_result = to_amounts_by_order(
    component_amounts=missing_component_amounts,
    components=components,
    component_key="Name",
)
print("[bold red]missing component result[/bold red]")
print(missing_component_result)
