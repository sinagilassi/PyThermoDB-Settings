# import libs
from pythermodb_settings import __version__
from pythermodb_settings.models import Component
from pythermodb_settings.utils import create_mixture_id
from rich import print

# version info
print(f"Version: {__version__}")

# NOTE: create a component
water = Component(name="Water", formula="H2O", state="l")
print(water)

# methanol
methanol = Component(name="Methanol", formula="CH4O", state="l")
# ethanol
ethanol = Component(name="Ethanol", formula="C2H6O", state="l")
# methane
methane = Component(name="Methane", formula="CH4", state="g")

# NOTE: create a component with new keyword argument
comp2 = Component(name="Ethanol", formula="C2H6O", state="l", CAS="64-17-5")
print(comp2)

# NOTE: create a mixture id
mix_id = create_mixture_id([water, comp2])
print(f"Mixture ID: {mix_id}")

# NOTE: create another mixture id
# ! default (by name)
mix_id2 = create_mixture_id([methanol, water, ethanol, methane])
print(f"Mixture ID 2: {mix_id2}")

# ! by formula
mix_id3 = create_mixture_id(
    [methanol, water, ethanol, methane], mixture_key='Formula')
print(f"Mixture ID 3 (by formula): {mix_id3}")

# ! by formula-state
mix_id4 = create_mixture_id(
    [methanol, water, ethanol, methane], mixture_key='Formula-State')
print(f"Mixture ID 4 (by formula-state): {mix_id4}")

# ! by name-state
mix_id5 = create_mixture_id(
    [methanol, water, ethanol, methane], mixture_key='Name-State')
print(f"Mixture ID 5 (by name-state): {mix_id5}")
