# import libs
from pythermodb_settings.models import Component
from rich import print

# NOTE: create a component with an automatically derived charge
component = Component(
    name="Glycine zwitterion",
    formula="NH3{+}-CH2-COO{-}",
    state="s",
)
print(component)

# ! species helpers
print("Has cation species type:", component.has_species_type("cation"))
print("Is neutral:", component.is_neutral())
print("Is cation:", component.is_cation())
print("Is anion:", component.is_anion())
print("Is radical:", component.is_radical())
print("Is zwitterion:", component.is_zwitterion())
print("Is ionic:", component.is_ionic())

# ! charge helpers
print("Charge centers:", component.get_charge_centers())
print("Net charge:", component.get_net_charge())
print("Has charge centers:", component.has_charge_centers())
print("Has internal charges:", component.has_internal_charges())
print("Charge center count:", component.get_charge_center_count())
print("Positive charge count:", component.get_positive_charge_count())
print("Negative charge count:", component.get_negative_charge_count())
print("Total positive charge:", component.get_total_positive_charge())
print("Total negative charge:", component.get_total_negative_charge())
print("Is charged:", component.is_charged())

# ! radical helpers
print("Radical count:", component.get_radical_count())
print("Has radical centers:", component.has_radical_centers())
print("Is radical ion:", component.is_radical_ion())

# ! phase helpers
print("Is gas:", component.is_gas())
print("Is liquid:", component.is_liquid())
print("Is solid:", component.is_solid())
print("Is aqueous:", component.is_aqueous())

# ! formula helpers
print("Base formula:", component.get_base_formula())
print("Has annotations:", component.has_annotations())

# ! identity helpers
print("Name-state:", component.get_name_state())
print("Formula-state:", component.get_formula_state())
print("Name-formula:", component.get_name_formula())
print("Name-formula-state:", component.get_name_formula_state())
