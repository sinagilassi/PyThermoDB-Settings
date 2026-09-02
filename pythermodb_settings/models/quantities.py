# import libs
from typing import Mapping
from pythermodb_settings.models.conditions import CustomProp


# SECTION: Component quantity models
ComponentAmounts = Mapping[str, CustomProp | float | int]
ComponentMoles = Mapping[str, CustomProp | float | int]
ComponentMasses = Mapping[str, CustomProp | float | int]
ComponentVolumes = Mapping[str, CustomProp | float | int]
