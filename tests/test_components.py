import unittest

from pythermodb_settings.models import Component
from pythermodb_settings.utils.component_utils import (
    extract_components_values,
    find_component_key_by_id,
)


class ComponentChargeParsingTest(unittest.TestCase):
    def test_component_derives_charge_and_species_type_from_formula(self) -> None:
        cases = [
            ("Fe{3+}", 3, ["cation"]),
            ("Br{-}", -1, ["anion"]),
            ("CH3{*}", 0, ["neutral", "radical"]),
            ("CH3{*+}", 1, ["cation", "radical"]),
            ("CH3{*-}", -1, ["anion", "radical"]),
            ("NH3{+}-CH2-COO{-}", 0, ["zwitterion"]),
        ]

        for formula, charge, species_type in cases:
            with self.subTest(formula=formula):
                component = Component(
                    name="component", formula=formula, state="s")

                self.assertEqual(component.charge, charge)
                self.assertEqual(component.species_type, species_type)

    def test_component_rejects_inconsistent_explicit_charge(self) -> None:
        with self.assertRaisesRegex(ValueError, "inconsistent"):
            Component(
                name="Methyl radical cation",
                formula="CH3{*+}",
                state="s",
                charge=0,
            )

    def test_component_species_predicates(self) -> None:
        cases = [
            ("H2O", {"is_neutral": True, "is_ionic": False}),
            ("Fe{3+}", {"is_cation": True, "is_ionic": True}),
            ("Br{-}", {"is_anion": True, "is_ionic": True}),
            ("CH3{*}", {"is_neutral": True, "is_radical": True}),
            (
                "NH3{+}-CH2-COO{-}",
                {"is_zwitterion": True, "is_ionic": False},
            ),
        ]

        for formula, predicates in cases:
            with self.subTest(formula=formula):
                component = Component(
                    name="component", formula=formula, state="s")

                for predicate, expected in predicates.items():
                    self.assertEqual(getattr(component, predicate)(), expected)

        self.assertTrue(component.has_species_type("zwitterion"))

    def test_component_attribute_method_resolves_fields_and_helpers(self) -> None:
        component = Component(
            name="Water",
            formula="H2O",
            state="l",
            mole_fraction=0.25,
            CAS="7732-18-5",
        )

        self.assertEqual(component.get_attribute_method(
            "mole_fraction")(), 0.25)
        self.assertEqual(component.get_attribute_method(
            "base_formula")(), "H2O")
        self.assertEqual(component.get_attribute_value(
            "species_type"), ["neutral"])
        self.assertTrue(component.get_attribute_method("liquid")())
        self.assertEqual(component.get_attribute_value("CAS"), "7732-18-5")

    def test_component_summary_attributes_returns_descriptions(self) -> None:
        attributes = Component.summary_attributes()

        self.assertIn("name", attributes)
        self.assertIn("mole_fraction", attributes)
        self.assertIn("net_charge", attributes)
        self.assertIn("ionic", attributes)
        self.assertEqual(attributes["net_charge"],
                         "Net charge of the component.")
        self.assertEqual(
            attributes["name"],
            "Name of the component",
        )

    def test_find_component_key_by_id_returns_matching_key(self) -> None:
        components = [
            Component(name="Water", formula="H2O", state="l"),
            Component(name="Ethanol", formula="C2H6O", state="l"),
        ]

        cases = [
            ("Water", "Name"),
            ("H2O", "Formula"),
            ("Water-l", "Name-State"),
            ("H2O-l", "Formula-State"),
            ("Water-H2O", "Name-Formula"),
            ("Water-H2O-l", "Name-Formula-State"),
            ("H2O-Water-l", "Formula-Name-State"),
        ]

        for component_id, expected_key in cases:
            with self.subTest(component_id=component_id):
                self.assertEqual(
                    find_component_key_by_id(component_id, components),
                    expected_key,
                )

    def test_find_component_key_by_id_supports_case_and_strict_mode(self) -> None:
        components = [Component(name="Water", formula="H2O", state="l")]

        self.assertEqual(
            find_component_key_by_id(
                "water-l",
                components,
                case_sensitive=False,
            ),
            "Name-State",
        )
        self.assertIsNone(
            find_component_key_by_id("Water", components, mode="strict")
        )
        self.assertIsNone(
            find_component_key_by_id("Missing", components)
        )

    def test_extract_component_values_uses_component_attribute(self) -> None:
        components = [
            Component(
                name="Ethanol",
                formula="C2H6O",
                state="l",
                mole_fraction=0.4,
            ),
            Component(
                name="Water",
                formula="H2O",
                state="l",
                mole_fraction=0.6,
            ),
        ]

        values, value_list = extract_component_values(
            attribute_name="mole_fraction",
            components=components,
            component_key="Name",
        )

        self.assertEqual(values, {"Ethanol": 0.4, "Water": 0.6})
        self.assertEqual(value_list, [0.4, 0.6])


if __name__ == "__main__":
    unittest.main()
