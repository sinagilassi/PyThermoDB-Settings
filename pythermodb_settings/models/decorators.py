# import libs
from typing import Any
from pydantic import BaseModel, ConfigDict

# SECTION:  Calculation Signature


class CalculationSignature(BaseModel):
    """
    Dynamically resolved technical signature of a calculation function.

    Attributes
    ----------
    parameters : dict[str, Any]
        Mapping of parameter names to their types.
    return_type : Any
        The return type of the calculation function.
    """

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )

    parameters: dict[str, Any]
    return_type: Any
