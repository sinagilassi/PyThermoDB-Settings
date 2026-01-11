from pathlib import Path
from pythermodb_settings.models import Component
from pythermodb_settings.references.component_extractor import ComponentExtractor


ce = ComponentExtractor()
# H2O
water = Component(name="water", formula="H2O", state="g")
# CO2
CO2 = Component(name="carbon dioxide", formula="CO2", state="g")

ce.load_ref("private/reference_content.yaml")  # load once at startup

result = ce.filter_components_from_data(
    components=[water, CO2],
    component_key="Name-Formula",
    separator_symbol="-",
    save_reference=True,
    output_path="private/filtered.yaml",
    mode="log"
)
print(result["matched"], result["missing"])
