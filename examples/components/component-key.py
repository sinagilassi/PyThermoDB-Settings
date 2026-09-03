# import libs
from pythermodb_settings.models import Component
from pythermodb_settings.utils import (
    find_component_key_by_id,
    set_component_id,
)
from rich import print

# NOTE: create components
components = [
    Component(name="Water", formula="H2O", state="l"),
    Component(name="Ethanol", formula="C2H6O", state="l"),
]

# NOTE: find the exact ComponentKey from component identifiers
component_ids = [
    set_component_id(components[0], "Name"),
    set_component_id(components[0], "Formula"),
    set_component_id(components[0], "Name-State"),
    set_component_id(components[0], "Formula-State"),
    set_component_id(components[0], "Name-Formula"),
    set_component_id(components[0], "Name-Formula-State"),
    set_component_id(components[0], "Formula-Name-State"),
]

for component_id in component_ids:
    component_key = find_component_key_by_id(
        id=component_id,
        components=components,
    )
    print({
        "component_id": component_id,
        "component_key": component_key,
    })

# NOTE: case-insensitive matching
component_key = find_component_key_by_id(
    id="water-l",
    components=components,
    case_sensitive=False,
)
print({
    "component_id": "water-l",
    "component_key": component_key,
})