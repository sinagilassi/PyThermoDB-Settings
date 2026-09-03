from pythermodb_settings.utils import extract_components_values
from pythermodb_settings.models import Component
import sys
from pathlib import Path
from rich import print

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


components = [
    Component(
        name="Ethanol",
        formula="C2H6O",
        state="l",
        mole_fraction=0.25,
        CAS="64-17-5",
    ),
    Component(
        name="Water",
        formula="H2O",
        state="l",
        mole_fraction=0.70,
        CAS="7732-18-5",
    ),
    Component(
        name="Sodium",
        formula="Na{+}",
        state="aq",
        mole_fraction=0.05,
        CAS="7440-23-5",
    ),
    Component(
        name="Chloride",
        formula="Cl{-}",
        state="aq",
        mole_fraction=0.05,
        CAS="7440-70-2",
    )
]

# Resolve one component attribute to its relevant zero-argument method.
component = components[2]
charge_method = component.get_attribute_method("net_charge")
print("Sodium net charge:", charge_method())

# Direct fields and extra fields can be read the same way.
print("Water mole fraction:",
      components[1].get_attribute_value("mole_fraction"))
print("Water CAS:", components[1].get_attribute_value("CAS"))

# Extract an attribute from every component and re-key the result.
mole_fraction_values = extract_components_values(
    attribute_name="mole_fraction",
    components=components,
    component_key="Formula-State",
    sort_by_components_order=True,
)

if mole_fraction_values is None:
    raise ValueError("Could not extract component mole_fraction values.")

values_by_formula_state, values_list = mole_fraction_values

print("Mole fractions by Formula-State:", values_by_formula_state)
print("Mole fractions list:", values_list)

# Helper methods can also be extracted by their short attribute name.
ionic_values = extract_components_values(
    attribute_name="ionic",
    components=components,
    component_key="Name",
)

if ionic_values is None:
    raise ValueError("Could not extract component ionic values.")

values_by_name, ionic_list = ionic_values

print("Ionic flags by Name:", values_by_name)
print("Ionic flags list:", ionic_list)

# Extract net charge
net_charge_values = extract_components_values(
    attribute_name="net_charge",
    components=components,
    component_key="Formula-State",
)

if net_charge_values is None:
    raise ValueError("Could not extract component net charge values.")

values_by_formula_state_charge, net_charge_list = net_charge_values

print("Net charges by Formula-State:", values_by_formula_state_charge)
print("Net charges list:", net_charge_list)
