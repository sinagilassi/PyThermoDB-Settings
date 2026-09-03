# import libs
from rich import print
from pythermodb_settings.models import Component

# NOTE: Define a component
ethanol = Component(
    name="Ethanol",
    formula="C2H6O",
    state="l",
    mole_fraction=0.25,
)

# Print the component's attributes
print(ethanol.summary_attributes())
