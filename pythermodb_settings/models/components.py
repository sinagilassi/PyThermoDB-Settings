# import libs
from typing import (
    Literal
)
from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


class Component(BaseModel):
    """Component model for input validation"""
    name: str = Field(..., description="Name of the component")
    formula: str = Field(..., description="Chemical formula of the component")
    state: Literal['g', 'l', 's', 'aq'] = Field(
        ...,
        description="State of the component: 'g' for gas, 'l' for liquid, 's' for solid, 'aq' for aqueous"
    )
    mole_fraction: float = Field(
        default=1.0,
        description="Mole fraction of the component in a mixture, if applicable"
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class Temperature(BaseModel):
    """Temperature model for input validation"""
    value: float = Field(..., description="Temperature value")
    unit: str = Field(..., description="Temperature unit, e.g., 'K', 'C', 'F'")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )


class Pressure(BaseModel):
    """Pressure model for input validation"""
    value: float = Field(..., description="Pressure value")
    unit: str = Field(
        ...,
        description="Pressure unit, e.g., 'bar', 'atm', 'Pa'"
    )

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
