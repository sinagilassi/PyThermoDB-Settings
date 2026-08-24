# import libs
from rich import print
import pycuc
# ! pythermodb_settings imports
from pythermodb_settings.models import Component, CustomProp, MixtureComposition
from pythermodb_settings.utils import set_component_composition, component_composition

# =======================================
# ✅ unit conversion settings
# =======================================
# NOTE: create unit conversion function using pycuc
unit_conversion_fn = pycuc.convert_from_to

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
# ! composition (mole fraction)
composition = {
    'carbon dioxide': CustomProp(value=0.5, unit=''),
    'hydrogen': CustomProp(value=0.3, unit=''),
    'methanol': CustomProp(value=0.1, unit=''),
    'ethanol': CustomProp(value=0.1, unit=''),
}

# mixture composition
mixture_composition = MixtureComposition(
    basis='mole_fraction',
    components=components,
    compositions=composition,
)

# component composition
res = component_composition(
    mixture_composition=mixture_composition,
    unit_conversion_fn=unit_conversion_fn,
    identifier_mode='strict'  # default
)
print(f"[bold green]strict mode[/bold green]")
print(res)

# component composition
res = component_composition(
    mixture_composition=mixture_composition,
    unit_conversion_fn=unit_conversion_fn,
    identifier_mode='normal'  # or 'strict'
)
print(f"[bold blue]normal mode[/bold blue]")
print(res)


# ! composition (mass)
composition = {
    'carbon dioxide-g': CustomProp(value=0.5, unit='g'),
    'hydrogen-g': CustomProp(value=0.0003, unit='kg'),
    'methanol-g': CustomProp(value=0.1, unit='g'),
    'ethanol-g': CustomProp(value=0.1, unit='g'),
}

# mixture composition
mixture_composition = MixtureComposition(
    basis='mass',
    components=components,
    compositions=composition,
)

# component composition
res = component_composition(
    mixture_composition=mixture_composition,
    to_unit='kg',
    unit_conversion_fn=unit_conversion_fn,
    identifier_mode='strict'  # default
)
print(f"[bold green]strict mode[/bold green]")
print(res)

# ! set component composition
res = set_component_composition(
    mixture_composition=mixture_composition,
    to_unit='kg',
    unit_conversion_fn=unit_conversion_fn,
    identifier_mode='strict'  # default
)
print(f"[bold blue]set component composition[/bold blue]")
print(res)
