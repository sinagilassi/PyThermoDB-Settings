# import libs
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from rich import print
from pythermodb_settings.models import Mixture, Component
from pythermodb_settings.utils import generate_mixture_references

# NOTE: create ionic components
comp1 = Component(name="Iron(III)", formula="Fe{3+}", state="s")
comp2 = Component(name="Iron(III)", formula="Fe{3+}", state="aq")
comp3 = Component(name="Aluminum(III)", formula="Al{3+}", state="s")
comp4 = Component(name="Bromide", formula="Br{-}", state="s")
comp5 = Component(name="Bromide", formula="Br{-}", state="aq")

# NOTE: create a mixture
mixture_1: Mixture = [comp1, comp4]
print("Mixture 1:", mixture_1)

# mixture 2
mixture_2: Mixture = [comp2, comp5]
print("Mixture 2:", mixture_2)

# mixture 3
mixture_3: Mixture = [comp1, comp2, comp3, comp4, comp5]
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
    mixture_key="Formula-State",
    mixture_keys=[
        "Formula-State",
        "Name-State",
        "Name-Formula-State",
    ],
)
print("mixture references custom")
print(mixture_refs_custom)

# ! empty mixture list
mixture_refs_empty = generate_mixture_references(
    mixtures=[],
    mixture_key="Name"
)
print("mixture references empty")
print(mixture_refs_empty)
