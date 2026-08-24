# import libs
from typing import List
from pythermodb_settings.models import Component, ComponentKey
from pythermodb_settings.utils import set_component_id
from rich import print

# NOTE: create a component
comp = Component(name="Iron(III)", formula="Fe{3+}", state="s", charge=3)
print(comp)

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
    r = set_component_id(comp, key)
    print(f"Component ID ({key}): {r}")
