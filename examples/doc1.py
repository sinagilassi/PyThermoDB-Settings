# import libs
from pythermodb_settings import __version__
from pythermodb_settings.models import Component
from rich import print

# version info
print(f"Version: {__version__}")

# create a component
comp = Component(name="Water", formula="H2O", state="l")
print(comp)
