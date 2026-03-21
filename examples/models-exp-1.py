# import libs
from pythermodb_settings.models import CustomProperty
from rich import print

# NOTE: create a custom property
custom_prop = CustomProperty(
    value=100.0,
    unit='J/mol.K',
    symbol='Cp',
    name='Heat Capacity'
)
print(custom_prop)

custom_prop = CustomProperty(
    value=100.0,
    unit='J/mol.K',
    symbol='Cp'
)
print(custom_prop)
