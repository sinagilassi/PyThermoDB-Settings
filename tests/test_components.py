import unittest

from pythermodb_settings.models import Component


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


if __name__ == "__main__":
    unittest.main()
