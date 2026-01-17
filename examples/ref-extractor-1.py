from pathlib import Path
from pythermodb_settings.models import Component
from pythermodb_settings.references import (
    extract_reference_components,
    check_reference_component_availability
)


# H2O
water = Component(name="dihydrogen monoxide", formula="H2O", state="g")
# CO2
CO2 = Component(name="carbon dioxide", formula="CO2", state="g")

# --------------------------------------------------------------
# SECTION: Check component availability in reference file
# --------------------------------------------------------------
availability_result = check_reference_component_availability(
    reference=Path("private/reference_content.yaml"),
    component_keys=['H2O', 'CO2', 'N2b'],
    components=[water, CO2],
    component_key="Name",
    separator_symbol="-",
    case=None,
    renumber=False
)
print(availability_result)


# --------------------------------------------------------------
# SECTION: Extract components from reference file
# --------------------------------------------------------------
result = extract_reference_components(
    reference_file=Path("private/reference_content.yaml"),
    components=[water, CO2],
    component_key="Name-Formula",    # or any ComponentKey variant
    separator_symbol="-",
    case=None,
    save_reference=True,
    output_path="private/filtered.yaml",
    mode="log"
)
print(result["matched"], result["missing"], result["saved_to"])
