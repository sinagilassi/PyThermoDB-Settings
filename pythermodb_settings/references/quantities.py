from __future__ import annotations

from collections.abc import Iterator, Mapping
from functools import lru_cache
from importlib.resources import files

import yaml

from pythermodb_settings.models.quantity import (
    QuantityDefinition,
    QuantityRef,
    QuantityRegistryData,
)


class QuantityRegistry(Mapping[str, QuantityDefinition]):
    """
    Read-only mapping of canonical quantity definitions.

    Attributes
    ----------
    _quantities : dict[str, QuantityDefinition]
        Internal storage of quantity definitions keyed by their canonical keys.

    Methods
    -------
    __getitem__(key: str) -> QuantityDefinition
        Retrieve a quantity definition by its canonical key.
    __iter__() -> Iterator[str]
        Iterate over the canonical keys of the quantity definitions.
    __len__() -> int
        Return the number of quantity definitions.
    get_symbol(key: str) -> str
        Return the canonical symbol for a quantity key.
    get_description(key: str) -> str
        Return the canonical description for a quantity key.
    ref(key: str) -> QuantityRef
        Return resolved metadata for a quantity key.
    find_by_symbol(symbol: str) -> tuple[QuantityRef, ...]
        Return every registered quantity that uses the given symbol.
    """

    def __init__(
        self,
        quantities: dict[str, QuantityDefinition],
    ) -> None:
        self._quantities = dict(quantities)

    def __getitem__(self, key: str) -> QuantityDefinition:
        try:
            return self._quantities[key]
        except KeyError as exc:
            raise KeyError(
                f"Unknown quantity key: {key!r}"
            ) from exc

    def __iter__(self) -> Iterator[str]:
        return iter(self._quantities)

    def __len__(self) -> int:
        return len(self._quantities)

    def get_symbol(self, key: str) -> str:
        """Return the canonical symbol for a quantity key."""
        return self[key].symbol

    def get_description(self, key: str) -> str:
        """Return the canonical description for a quantity key."""
        return self[key].description

    def ref(self, key: str) -> QuantityRef:
        """Return resolved metadata for a quantity key."""
        quantity = self[key]

        return QuantityRef(
            key=key,
            symbol=quantity.symbol,
            description=quantity.description,
            domain=quantity.domain,
            quantity_type=quantity.quantity_type,
            basis=quantity.basis,
            phase=quantity.phase,
            namespace=quantity.namespace,
            index=quantity.index,
        )

    def find_by_symbol(
        self,
        symbol: str,
    ) -> tuple[QuantityRef, ...]:
        """
        Return every registered quantity that uses *symbol*.

        Symbols are not required to be globally unique because some model
        parameters are context-dependent. Quantity keys remain the canonical
        identifiers.
        """
        return tuple(
            self.ref(key)
            for key, quantity in self._quantities.items()
            if quantity.symbol == symbol
        )


@lru_cache(maxsize=1)
def load_quantity_registry() -> QuantityRegistry:
    """
    Load, validate, and cache the packaged quantity registry.

    The YAML file is read once per Python process. All downstream packages
    should consume ``registry`` instead of opening the YAML file directly.
    """
    path = files("pythermodb_settings.configs").joinpath(
        "quantities.yml"
    )

    with path.open("r", encoding="utf-8") as stream:
        raw = yaml.safe_load(stream)

    data = QuantityRegistryData.model_validate(raw)

    return QuantityRegistry(data.quantities)


registry = load_quantity_registry()
