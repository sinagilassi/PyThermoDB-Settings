# import libs
from typing import Protocol


class UnitConversionFn(Protocol):
    """
    Callable unit conversion interface used by ``build_inputs``.

    The callable must accept a numeric value, a source unit, and a target unit,
    then return the value converted to the target unit. Callers must ensure the
    provided conversion function supports every unit pair that may appear in the
    equation input definitions and runtime inputs.
    """

    def __call__(
        self,
        *,
        value: float,
        from_unit: str,
        to_unit: str,
    ) -> float:
        ...
