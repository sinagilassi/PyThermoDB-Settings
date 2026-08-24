# import libs
from pprint import pprint
# ! pythermodb_settings imports
from pythermodb_settings.models import Component
from pythermodb_settings.utils import (
    set_mixture_mole_fraction,
    set_mixture_mass_fraction,
    set_mixture_volume_fraction,
    set_mixture_molar_concentration,
    set_mixture_mass_concentration,
    set_mixture_molality,
    set_mixture_partial_pressure,
    set_mixture_moles,
    set_mixture_mass,
    set_mixture_volume,
)

# =======================================
# ✅ create component
# =======================================
# carbon dioxide
CO2 = Component(
    name='carbon dioxide',
    formula='CO2',
    state='g',
)

# Hydrogen
H2 = Component(
    name='hydrogen',
    formula='H2',
    state='g',
)

# methanol
CH3OH = Component(
    name='methanol',
    formula='CH3OH',
    state='g',
)

# ethanol
C2H5OH = Component(
    name='ethanol',
    formula='C2H5OH',
    state='g',
)

# ! components
components = [CO2, H2, CH3OH, C2H5OH]

# =======================================
# ✅ create mixture composition
# =======================================
# Component identifiers must match the selected identifier mode.
composition = {
    'carbon dioxide-g': 0.5,
    'hydrogen-g': 0.3,
    'methanol-g': 0.1,
    'ethanol-g': 0.1,
}

composition_setters = {
    'mole fraction': set_mixture_mole_fraction,
    'mass fraction': set_mixture_mass_fraction,
    'volume fraction': set_mixture_volume_fraction,
    'molar concentration': set_mixture_molar_concentration,
    'mass concentration': set_mixture_mass_concentration,
    'molality': set_mixture_molality,
    'partial pressure': set_mixture_partial_pressure,
    'moles': set_mixture_moles,
    'mass': set_mixture_mass,
    'volume': set_mixture_volume,
}

for basis, setter in composition_setters.items():
    print(f'\n{basis}:')
    pprint(setter(composition=composition, components=components))
