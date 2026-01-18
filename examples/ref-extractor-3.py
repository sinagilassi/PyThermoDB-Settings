from pathlib import Path
from typing import List
from pythermodb_settings.models import Component
from pythermodb_settings.references import (
    extract_reference_components,
    check_reference_component_availability
)

# -------------------------------------------------------------------
# SECTION: components to build thermodb for
# -------------------------------------------------------------------
# NOTE: components
components: List[Component] = [
    Component(name='benzene', formula='C6H6', state='g'),
    Component(name='toluene', formula='C7H8', state='g'),
    Component(name='ethanol', formula='C2H6O', state='g'),
    Component(name='methane', formula='CH4', state='g'),
    Component(name="methanol", formula='CH4O', state='g'),
    Component(name='propane', formula='C3H8', state='g'),
    Component(name='ethane', formula='C2H6', state='g'),
    Component(name='carbon dioxide', formula='CO2', state='g'),
    Component(name='carbon monoxide', formula='CO', state='g'),
    Component(name='dinitrogen', formula='N2', state='g'),
    Component(name='dioxygen', formula='O2', state='g'),
    Component(name='water', formula='H2O', state='g'),
    Component(name='dihydrogen', formula='H2', state='g'),
]

# -------------------------------------------------------------------
# SECTION: Check reference component availability
# -------------------------------------------------------------------
availability_results = check_reference_component_availability(
    reference="private/reference_content.yaml",
    component_keys=['C6H6', 'C7H8', 'C2H6O', 'CH4', 'CH4O',
                    'C3H8', 'C2H6', 'CO2', 'CO', 'N2', 'O2', 'H2O', 'H2'],
    component_key="Formula",
    separator_symbol="-",
    case=None,
    renumber=False
)
print(f"availability_results:")
print(availability_results)

# components matched: availability_results['matched_components']
components_matched: List[Component] = availability_results['matched_components']
print(f"components matched: {components_matched}")

# -------------------------------------------------------------------
# SECTION: extract reference components
# -------------------------------------------------------------------
result = extract_reference_components(
    reference_file=Path("private/reference_content.yaml"),
    components=components_matched,
    component_key="Formula",    # or any ComponentKey variant
    separator_symbol="-",
    case=None,
    save_reference=True,
    output_path="private/filtered.yaml",
    mode="log"
)
print(result["matched"], result["missing"], result["saved_to"])
