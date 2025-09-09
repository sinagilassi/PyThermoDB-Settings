# import libs
from pydantic import BaseModel, Field, ConfigDict


class ComponentRule(BaseModel):
    DATA: dict[str, str] = Field(
        default_factory=dict, description="Data rules")
    EQUATIONS: dict[str, str] = Field(
        default_factory=dict, description="Equation rules")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
    )
