# import libs
from typing import List
from pythermodb_settings.models import Component, MixtureKey
from pythermodb_settings.utils import create_component_ids, create_mixture_ids_with_keys
from rich import print

# NOTE: create a component
comp = Component(name="Water", formula="H2O", state="l")
print(comp)

comp2 = Component(name="Ethanol", formula="C2H6O", state="l")
print(comp2)

comp3 = Component(name="Methanol", formula="CH3OH", state="l")
print(comp3)

# SECTION: create a components ids
components = [comp, comp3, comp2]
components_ids = create_component_ids(
    components,
)
print(components_ids)

# ! sort alphabetically
components_ids_sorted = create_component_ids(
    components,
    sort_alphabetically=True
)
print(components_ids_sorted)

# SECTION: create a mixture ids
mixture_keys: List[MixtureKey] = [
    "Name", "Formula", "Name-State", "Formula-State"
]

# NOTE: create mixture ids based on the specified mixture keys
# ! as is
mixture_ids_as_is = create_mixture_ids_with_keys(
    components=components,
    mixture_keys=mixture_keys,
    sort_alphabetically=False
)
print(f"[blue]Mixture IDs (as is):[/blue]")
print(mixture_ids_as_is)


# ! sort alphabetically
mixture_ids = create_mixture_ids_with_keys(
    components=components,
    mixture_keys=mixture_keys,
    sort_alphabetically=True
)
print(f"[yellow]Mixture IDs (sorted alphabetically):[/yellow]")
print(mixture_ids)
