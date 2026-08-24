from pathlib import Path
from pythermodb_settings.models import Component
from pythermodb_settings.references.component_extractor import ComponentExtractor

ce = ComponentExtractor()
# H2O
water = Component(name="water", formula="H2O", state="g")
# CO2
CO2 = Component(name="carbon dioxide", formula="CO2", state="g")

result = ce.filter_components_from_file(
    Path("private/reference_content.yaml"),
    components=[water, CO2],
    component_key="Name-Formula",    # or any ComponentKey variant
    separator_symbol="-",
    case=None,
    save_reference=True,
    output_path="private/filtered.yaml",
    mode="log"
)
print(result["matched"], result["missing"], result["saved_to"])
