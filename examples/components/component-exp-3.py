# import libs
from pythermodb_settings.utils import find_component_by_id, find_components_by_ids
from pythermodb_settings.models import Component
from rich import print
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

# ! pythermodb_settings imports

# NOTE: create component
# ! propane
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

# water
H2O = Component(
    name='water',
    formula='H2O',
    state='g',
)

# Carbon monoxide
CO = Component(
    name='carbon monoxide',
    formula='CO',
    state='g',
)

# ethylene
C2H4 = Component(
    name='ethylene',
    formula='C2H4',
    state='g',
)

# ethane
C2H6 = Component(
    name='ethane',
    formula='C2H6',
    state='g',
)

# components list
components = [CO2, H2, CH3OH, C2H5OH, H2O, CO, C2H4, C2H6]

# NOTE: find component by id
component_id = 'C2H5OH-g'
res = find_component_by_id(
    id=component_id,
    components=components
)
print(res)

# NOTE: component ids
component_ids = [
    "C2H5OH-g",
    "water-g",
    "Water-g",
    "water-l",
    "CO2-g",
    "C2H6-g",
    "XYZ-g"  # non-existent component
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
    "C2H5OH-g",
    "water-g",
    # "Water-g",
    "CO2-g",
    "C2H6-g",
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
