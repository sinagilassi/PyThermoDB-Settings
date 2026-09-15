import unittest

from pythermodb_settings.models.quantity import QuantityDefinition
from pythermodb_settings.references.quantities import QuantityRegistry
from pythermodb_settings.utils import tools
from pythermodb_settings.utils.tools import to_annotated_value


class ToAnnotatedValueTest(unittest.TestCase):
    def test_to_annotated_value_can_resolve_metadata_by_symbol(self) -> None:
        result = to_annotated_value(
            value=298.15,
            name="provided_name",
            description="Provided description",
            unit="K",
            symbol="T",
            check_symbol_in_registry=True,
        )

        self.assertEqual(result.name, "temperature")
        self.assertEqual(result.description, "System temperature")
        self.assertEqual(result.symbol, "T")

    def test_to_annotated_value_uses_provided_metadata_when_disabled(self) -> None:
        result = to_annotated_value(
            value=298.15,
            name="provided_name",
            description="Provided description",
            unit="K",
            symbol="T",
        )

        self.assertEqual(result.name, "provided_name")
        self.assertEqual(result.description, "Provided description")

    def test_to_annotated_value_uses_provided_metadata_for_unknown_symbol(self) -> None:
        result = to_annotated_value(
            value=1.0,
            name="custom",
            description="Custom quantity",
            symbol="unknown_symbol",
            check_symbol_in_registry=True,
        )

        self.assertEqual(result.name, "custom")
        self.assertEqual(result.description, "Custom quantity")
        self.assertEqual(result.symbol, "unknown_symbol")

    def test_to_annotated_value_uses_provided_metadata_for_ambiguous_symbol(
        self,
    ) -> None:
        original_registry = tools.registry
        tools.registry = QuantityRegistry(
            {
                "first": QuantityDefinition(
                    symbol="x",
                    description="First quantity",
                ),
                "second": QuantityDefinition(
                    symbol="x",
                    description="Second quantity",
                ),
            }
        )

        try:
            result = to_annotated_value(
                value=1.0,
                name="provided",
                description="Provided description",
                symbol="x",
                check_symbol_in_registry=True,
            )
        finally:
            tools.registry = original_registry

        self.assertEqual(result.name, "provided")
        self.assertEqual(result.description, "Provided description")


if __name__ == "__main__":
    unittest.main()
