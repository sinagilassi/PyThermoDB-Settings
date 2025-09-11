# import libs
from pythermodb_settings import __version__
from pythermodb_settings.models import Component
from rich import print

# version info
print(f"Version: {__version__}")

# NOTE: create a component
comp = Component(name="Water", formula="H2O", state="l")
print(comp)


# NOTE: create a component with new keyword argument
comp2 = Component(name="Ethanol", formula="C2H6O", state="l", CAS="64-17-5")
print(comp2)
