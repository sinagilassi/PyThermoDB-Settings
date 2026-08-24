# import libs
from pythermodb_settings.models import Component
from rich import print

# NOTE: create a component
comp = Component(name="Water", formula="H2O", state="l")
print(comp)

# NOTE: create a component with new property
initial_mole = {
    'value': 1.0,
    'unit': 'mol',
    'symbol': 'n',
    'name': 'Initial Mole'
}

comp2 = Component(name="Ethanol", formula="C2H6O", state="l", X=initial_mole)
print(comp2)
