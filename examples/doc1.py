# import libs
from pythermodb_settings import __version__
from pythermodb_settings.models import Component
from pythermodb_settings.utils import set_component_id
from rich import print

# version info
print(f"Version: {__version__}")

# NOTE: create a component
comp = Component(name="Water", formula="H2O", state="l")
print(comp)


# NOTE: create a component with new keyword argument
comp2 = Component(name="Ethanol", formula="C2H6O", state="l", CAS="64-17-5")
print(comp2)

# SECTION: set component id
# ! by name
print(set_component_id(
    component=comp,
    component_key='Name'
))
# ! by formula
print(set_component_id(
    component=comp2,
    component_key='Formula'
))
# ! by name-state
print(set_component_id(
    component=comp2,
    component_key='Name-State'
))
# ! by formula-state
print(set_component_id(
    component=comp2,
    component_key='Formula-State'
))
# ! by name-formula-state
print(set_component_id(
    component=comp2,
    component_key='Name-Formula-State'
))
# ! by formula-name-state
print(set_component_id(
    component=comp2,
    component_key='Formula-Name-State'
))
# ! upper
print(set_component_id(
    component=comp2,
    component_key='Name',
    case='upper'
))
# ! lower
print(set_component_id(
    component=comp2,
    component_key='Name',
    case='lower'
))
