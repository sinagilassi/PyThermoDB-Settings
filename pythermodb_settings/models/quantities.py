# import libs
from typing import TypeAlias
from collections.abc import Mapping, Sequence
from .conditions import ScalarValue


# SECTION: Component Quantity Models
ComponentAmounts: TypeAlias = Mapping[str, ScalarValue]
ComponentMoles: TypeAlias = Mapping[str, ScalarValue]
ComponentMasses: TypeAlias = Mapping[str, ScalarValue]
ComponentVolumes: TypeAlias = Mapping[str, ScalarValue]

# SECTION: Component Values Model
ComponentValues: TypeAlias = Mapping[str, ScalarValue] | Sequence[ScalarValue]
