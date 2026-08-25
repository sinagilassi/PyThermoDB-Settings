# import libs
from typing import List
from pythermodb_settings.models import Component, ComponentKey
from pythermodb_settings.utils import set_component_id
from rich import print

# NOTE: create a component
# ! with charge
comp_1 = Component(name="Iron(III)", formula="Fe{3+}", state="s", charge=3)
print(comp_1)

# ! without charge
comp_2 = Component(name="Iron(III)", formula="Fe{3+}", state="s")
print(comp_2)

# Al{3+}
comp_3 = Component(name="Aluminum(III)", formula="Al{3+}", state="s", charge=3)
print(comp_3)

# Bromide ion Br{-}
comp_4 = Component(name="Bromide", formula="Br{-}", state="s", charge=-1)
print(comp_4)

comp_5 = Component(name="Bromide", formula="Br{-}", state="s")
print(comp_5)

# Phosphate ion PO4{3-}
comp_6 = Component(name="Phosphate", formula="PO4{3-}", state="s", charge=-3)
print(comp_6)

comp_7 = Component(name="Phosphate", formula="PO4{3-}", state="s")
print(comp_7)

# Hydride ion H{-}
comp_8 = Component(name="Hydride", formula="H{-}", state="s", charge=-1)
print(comp_8)

comp_9 = Component(name="Hydride", formula="H{-}", state="s")
print(comp_9)

# Proton H{+}
comp_10 = Component(name="Proton", formula="H{+}", state="s", charge=1)
print(comp_10)

comp_11 = Component(name="Proton", formula="H{+}", state="s")
print(comp_11)
