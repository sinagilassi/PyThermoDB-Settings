# import libs
from pythermodb_settings.models import Mixture, Component, MixtureIdentity

# NOTE: create components
comp1 = Component(name="Water", formula="H2O", state="l")
comp2 = Component(name="Ethanol", formula="C2H6O", state="l")

# NOTE: create a mixture
mixture_1: Mixture = [comp1, comp2]
print("Mixture 1:", mixture_1)
