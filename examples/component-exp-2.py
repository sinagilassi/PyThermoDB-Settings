# import libs
from pythermodb_settings.models import Component
from pythermodb_settings.utils import build_component_mapper, build_components_mapper, is_component_key
from rich import print

# NOTE: create a component
comp = Component(name="Water", formula="H2O", state="l")
print(comp)

comp2 = Component(name="Ethanol", formula="C2H6O", state="l")
print(comp2)

# NOTE: create a mapper
mapper = build_component_mapper(comp)
print(mapper)

# NOTE: create a components mapper
components = [comp, comp2]
components_mapper = build_components_mapper(
    components,
    'Formula-State'
)
print(components_mapper)

# SECTION: type guard
component_keys = [
    'Name',
    'Formula  ',
    'State',
    'InvalidKey   ',
    'Name-State',
    'Formula-State    ',
    'State-Name',
    'Name-Formula-State',
    'InvalidKey-Name',
    'Name-InvalidKey',
]
print(is_component_key('Name'))  # True
print(is_component_key('InvalidKey'))  # False

for key in component_keys:
    print(f"{key}: {is_component_key(key)}")
