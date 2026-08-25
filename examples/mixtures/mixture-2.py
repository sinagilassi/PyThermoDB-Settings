# import libs
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from pythermodb_settings import __version__
from pythermodb_settings.models import Component
from pythermodb_settings.utils import create_mixture_id
from rich import print

# version info
print(f"Version: {__version__}")

# NOTE: create ionic components
iron_iii_s = Component(name="Iron(III)", formula="Fe{3+}", state="s")
print(iron_iii_s)

iron_iii_aq = Component(name="Iron(III)", formula="Fe{3+}", state="aq")
aluminum_iii_s = Component(name="Aluminum(III)", formula="Al{3+}", state="s")
bromide_s = Component(name="Bromide", formula="Br{-}", state="s")

# NOTE: create a component with new keyword argument
bromide_aq = Component(
    name="Bromide",
    formula="Br{-}",
    state="aq",
    source="aqueous ion",
)
print(bromide_aq)

# NOTE: create a mixture id
mix_id = create_mixture_id([iron_iii_s, bromide_s])
print(f"Mixture ID: {mix_id}")

# NOTE: create another mixture id
# ! default (by name)
mix_id2 = create_mixture_id(
    [iron_iii_s, iron_iii_aq, aluminum_iii_s, bromide_s, bromide_aq]
)
print(f"Mixture ID 2: {mix_id2}")

# ! by formula
mix_id3 = create_mixture_id(
    [iron_iii_s, iron_iii_aq, aluminum_iii_s, bromide_s, bromide_aq],
    mixture_key="Formula",
)
print(f"Mixture ID 3 (by formula): {mix_id3}")

# ! by formula-state
mix_id4 = create_mixture_id(
    [iron_iii_s, iron_iii_aq, aluminum_iii_s, bromide_s, bromide_aq],
    mixture_key="Formula-State",
)
print(f"Mixture ID 4 (by formula-state): {mix_id4}")

# ! by name-state
mix_id5 = create_mixture_id(
    [iron_iii_s, iron_iii_aq, aluminum_iii_s, bromide_s, bromide_aq],
    mixture_key="Name-State",
)
print(f"Mixture ID 5 (by name-state): {mix_id5}")

# ! by name-formula-state
mix_id6 = create_mixture_id(
    [iron_iii_s, iron_iii_aq, aluminum_iii_s, bromide_s, bromide_aq],
    mixture_key="Name-Formula-State",
)
print(f"Mixture ID 6 (by name-formula-state): {mix_id6}")
