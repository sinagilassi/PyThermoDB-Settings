from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class QuantityDefinition(BaseModel):
    """Canonical definition of a reusable physical quantity."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
        str_strip_whitespace=True,
    )

    symbol: str = Field(min_length=1)
    description: str = Field(min_length=1)

    domain: str | None = None
    quantity_type: str | None = None
    basis: str | None = None
    phase: str | None = None
    namespace: str | None = None
    index: Literal["component", "pair"] | None = None

    aliases: tuple[str, ...] = ()


class QuantityRegistryData(BaseModel):
    """Validated representation of the quantities YAML file."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    quantities: dict[str, QuantityDefinition]


class QuantityRef(BaseModel):
    """Resolved quantity metadata for use by calculation metadata and agents."""

    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    key: str
    symbol: str
    description: str

    domain: str | None = None
    quantity_type: str | None = None
    basis: str | None = None
    phase: str | None = None
    namespace: str | None = None
    index: Literal["component", "pair"] | None = None
