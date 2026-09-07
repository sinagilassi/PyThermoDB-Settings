# import libs
import numpy as np
from pythermodb_settings.utils import to_annotated_value
from pythermodb_settings.models import AnnotatedValue
import sys
from pathlib import Path
from typing import Any
from rich import print

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))


def print_annotated_value(
        title: str,
        value: Any,
        name: str | None = None,
        description: str | None = None,
        unit: str | None = None,
        symbol: str | None = None,
) -> None:
    print(f"\n{title}")
    print(
        to_annotated_value(
            value=value,
            name=name,
            description=description,
            unit=unit,
            symbol=symbol,
        ).model_dump()
    )


# A fully annotated scientific scalar.
print_annotated_value(
    "Enthalpy of formation",
    value=-285.83,
    name="standard_enthalpy_of_formation",
    description="Standard enthalpy of formation of liquid water at 298.15 K.",
    unit="kJ/mol",
    symbol="Hf",
)

# Dimensionless quantities can state their unit explicitly.
print_annotated_value(
    "Activity coefficient",
    value=1.21,
    name="activity_coefficient",
    description="Activity coefficient of sodium chloride.",
    unit="dimensionless",
    symbol="gamma",
)

# The value may also be a structured result with shared metadata.
print_annotated_value(
    "Component molalities",
    value={"Na+": 0.1, "Cl-": 0.1},
    name="component_molalities",
    description="Molality of each dissolved species.",
    unit="mol/kg",
)

# Metadata is optional when only the returned value is needed.
print_annotated_value("Simple value", value=True)

# The helper preserves the wrapped value type through AnnotatedValue[T].
enthalpy: AnnotatedValue[float] = to_annotated_value(
    value=-285.83,
    name="standard_enthalpy_of_formation",
    description="Standard enthalpy of formation of liquid water at 298.15 K.",
    unit="kJ/mol",
    symbol="Hf",
)
print("\nTyped scalar")
print(enthalpy.model_dump())

component_molalities: AnnotatedValue[dict[str, float]] = to_annotated_value(
    value={
        "Na+": 0.1,
        "Cl-": 0.1,
    },
    name="component_molalities",
    description="Molality of each dissolved species.",
    unit="mol/kg",
)
print("\nTyped structured value")
print(component_molalities.model_dump())

# A NumPy array can also be wrapped as an AnnotatedValue.

array_result: AnnotatedValue[np.ndarray] = to_annotated_value(
    value=np.array([1.0, 2.0, 3.0]),
    name="example_array",
    description="An example NumPy array.",
    unit="dimensionless",
)
print("\nTyped NumPy array")
print(array_result.model_dump())
