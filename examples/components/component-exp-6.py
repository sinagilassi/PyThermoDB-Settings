# import libs
from rich import print
from typing import List
from pythermodb_settings.models import Component
from pythermodb_settings.utils import find_component_by_id, find_components_by_ids
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

# ! pythermodb_settings imports

# NOTE: create ion components
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

# Phosphate
PO4 = Component(
    name='Phosphate',
    formula='PO4{3-}',
    state='s',
)

# Hydride
H = Component(
    name='Hydride',
    formula='H{-}',
    state='s',
)

# Proton
H_plus = Component(
    name='Proton',
    formula='H{+}',
    state='s',
)

# components list
components: List[Component] = [Fe3, Fe3_aq, Al3, Br, PO4, H, H_plus]

# NOTE: find component by id
component_id = 'Fe{3+}-s'
res = find_component_by_id(
    id=component_id,
    components=components
)
print(res)

# NOTE: component ids
component_ids = [
    "Fe{3+}-s",
    "Iron(III)-s",
    "iron(iii)-s",
    "Al{3+}-s",
    "Br{-}-s",
    "PO4{3-}-s",
    "H{+}-s",
    "Fe{3+}-aq",
    "XYZ-s",  # non-existent component
    "proton-s",  # Name-State
    "hydride-s",  # Name-State
    "Hydride-s",  # Name-State
]

# looping over component ids and find components
for cid in component_ids:
    res = find_component_by_id(
        id=cid,
        components=components,
        case_sensitive=False  # case-insensitive search
    )
    print(f"Component ID: {cid} -> Found: {res}")

# SECTION: find components by ids
component_ids = [
    "Fe{3+}-s",
    "Al{3+}-s",
    "Br{-}-s",
    "PO4{3-}-s",
    "proton-s",  # Name-State
    "Proton-s",  # Name-State
    "hydride-s",  # Name-State
    "Hydride-s",  # Name-State
]

# NOTE: find components by ids
# ! case sensitive is True
res = find_components_by_ids(
    ids=component_ids,
    components=components,
    case_sensitive=True
)
# print the results
print("Results of find_components_by_ids:")
print(res)

# ! case sensitive is False
res = find_components_by_ids(
    ids=component_ids,
    components=components,
    case_sensitive=False
)
# print the results
print("Results of find_components_by_ids (case-insensitive):")
print(res)
