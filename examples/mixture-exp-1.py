# import libs
from rich import print
from pythermodb_settings.models import Mixture, Component, MixtureIdentity
from pythermodb_settings.utils import generate_mixture_references

# NOTE: create components
comp1 = Component(name="Water", formula="H2O", state="l")
comp2 = Component(name="Ethanol", formula="C2H6O", state="l")
comp3 = Component(name="Methanol", formula="CH4O", state="l")

# NOTE: create a mixture
mixture_1: Mixture = [comp1, comp2]
print("Mixture 1:", mixture_1)

# mixture 2
mixture_2: Mixture = [comp1, comp3]
print("Mixture 2:", mixture_2)

# mixture 3
mixture_3: Mixture = [comp1, comp2, comp3]
print("Mixture 3:", mixture_3)

# SECTION: generate mixture references
# ! default
mixture_refs = generate_mixture_references(
    mixtures=[mixture_1, mixture_2, mixture_3],
    mixture_key="Name"
)
print("mixture references")
print(mixture_refs)

# ! custom configuration
mixture_refs_custom = generate_mixture_references(
    mixtures=[mixture_1, mixture_2, mixture_3],
    mixture_key="Formula",
    # mixture_keys=['Formula', 'Name-Formula'],
    # delimiter='-',
)
print("mixture references custom")
print(mixture_refs_custom)
