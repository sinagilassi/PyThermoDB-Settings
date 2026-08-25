# import libs
from typing import List
from pythermodb_settings.models import Component, ComponentKey
from pythermodb_settings.utils import set_component_id
from rich import print

# NOTE: create a component
# ! with charge
comp_1 = Component(name="Iron(III)", formula="Fe{3+}", state="s", charge=3)
print(comp_1)

# ! without charge
comp_2 = Component(name="Iron(III)", formula="Fe{3+}", state="s")
print(comp_2)

# NOTE: Set component ID
component_keys: List[ComponentKey] = [
    'Name',
    'Formula',
    'Name-State',
    'Formula-State',
    'Name-Formula',
    'Name-Formula-State',
    'Formula-Name-State'
]

for key in component_keys:
    r = set_component_id(
        component=comp_1,
        component_key=key
    )
    print(f"Component ID ({key}): {r}")
