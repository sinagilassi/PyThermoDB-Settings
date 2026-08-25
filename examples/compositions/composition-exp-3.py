# import libs
from rich import print
from typing import List
from pythermodb_settings.models import Component
import sys
from pathlib import Path
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

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


# =======================================
# ✅ create component
# =======================================
# Iron(III)
Fe3 = Component(
    name='Iron(III)',
    formula='Fe{3+}',
    state='s',
)

# >> aq
Fe3_aq = Component(
    name='Iron(III)',
    formula='Fe{3+}',
    state='aq',
)

# Aluminum(III)
Al3 = Component(
    name='Aluminum(III)',
    formula='Al{3+}',
    state='s',
)

# Bromide
Br = Component(
    name='Bromide',
    formula='Br{-}',
    state='s',
)

# ! components
components: List[Component] = [Fe3, Fe3_aq, Al3, Br]

# =======================================
# ✅ create mixture composition
# =======================================
# Component identifiers must match the selected identifier mode.
composition = {
    'Fe{3+}-s': 0.5,
    'Fe{3+}-aq': 0.3,
    'Al{3+}-s': 0.1,
    'Br{-}-s': 0.1,
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
    print(setter(composition=composition, components=components))
