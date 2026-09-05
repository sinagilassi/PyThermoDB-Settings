# import libs
from collections.abc import Mapping
from typing import Any, Dict
from pythermodb_settings.utils import config_components_values
from pythermodb_settings.models import Component
import sys
from pathlib import Path
from rich import print

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


# NOTE: define the ordered component list
components = [
    Component(name="Ethanol", formula="C2H6O", state="l"),
    Component(name="Water", formula="H2O", state="l"),
    Component(name="Sodium", formula="Na{+}", state="aq"),
]

# Input keys may use any identifier accepted by find_component_by_id.
values: Dict[str, Any] = {
    "Water-l": 0.70,
    "C2H6O-l": 0.25,
    "Sodium-aq": 0.05,
}

# mapping
values_mapping: Mapping[str, Any] = values.copy()

# ! true
configured_values = config_components_values(
    values=values,
    components=components,
    component_key="Formula-State",
    sort_by_components_order=True,
)

if configured_values is None:
    raise ValueError("Could not match all values to the supplied components.")

values_by_formula_state, values_list = configured_values

print("Values by Formula-State:", values_by_formula_state)
print("Configured values:", values_list)

# ! false
configured_values = config_components_values(
    values=values,
    components=components,
    component_key="Formula-State",
    sort_by_components_order=False,
)

if configured_values is None:
    raise ValueError("Could not match all values to the supplied components.")

values_by_formula_state, values_list = configured_values

print("Values by Formula-State (unsorted):", values_by_formula_state)
print("Configured values (unsorted):", values_list)

# ! mapping
configured_values = config_components_values(
    values=values_mapping,
    components=components,
    component_key="Formula-State",
    sort_by_components_order=True,
)

if configured_values is None:
    raise ValueError("Could not match all values to the supplied components.")

values_by_formula_state, values_list = configured_values

print("Values by Formula-State (mapping):", values_by_formula_state)
print("Configured values (mapping):", values_list)
