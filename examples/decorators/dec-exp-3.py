# import libs
from rich import print
from pythermodb_settings import registry

# SECTION: registry usage
# ! molarity
print(registry["molarity"].symbol)
# "Molar"

print(registry["molarity"].description)
# "Amount of solute per solution volume"

print(registry.ref("molarity"))


# SECTION: search usage
# ! molar-density
print(registry.find_by_symbol("Mol"))

# ! enthalpy of formation
print(registry.find_by_symbol("EnFo"))
