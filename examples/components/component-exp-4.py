# import libs
import sys
import time
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from pythermodb_settings.models import Component


CASES = [
    {
        "name": "Water",
        "formula": "H2O",
        "state": "l",
        "charge": 0,
        "species_type": ["neutral"],
    },
    {
        "name": "Dioxygen",
        "formula": "O2",
        "state": "g",
        "charge": 0,
        "species_type": ["neutral"],
    },
    {
        "name": "Carbon dioxide",
        "formula": "CO2",
        "state": "g",
        "charge": 0,
        "species_type": ["neutral"],
    },
    {
        "name": "Methanol",
        "formula": "CH4O",
        "state": "l",
        "charge": 0,
        "species_type": ["neutral"],
    },
    {
        "name": "Benzene",
        "formula": "C6H6",
        "state": "l",
        "charge": 0,
        "species_type": ["neutral"],
    },
    {
        "name": "Iron(III)",
        "formula": "Fe{3+}",
        "state": "s",
        "charge": 3,
        "species_type": ["cation"],
    },
    {
        "name": "Copper(II)",
        "formula": "Cu{2+}",
        "state": "aq",
        "charge": 2,
        "species_type": ["cation"],
    },
    {
        "name": "Calcium",
        "formula": "Ca{2+}",
        "state": "aq",
        "charge": 2,
        "species_type": ["cation"],
    },
    {
        "name": "Aluminum",
        "formula": "Al{3+}",
        "state": "aq",
        "charge": 3,
        "species_type": ["cation"],
    },
    {
        "name": "Cerium(IV)",
        "formula": "Ce{4+}",
        "state": "aq",
        "charge": 4,
        "species_type": ["cation"],
    },
    {
        "name": "Ammonium",
        "formula": "NH4{+}",
        "state": "aq",
        "charge": 1,
        "species_type": ["cation"],
    },
    {
        "name": "Sulfate",
        "formula": "SO4{2-}",
        "state": "aq",
        "charge": -2,
        "species_type": ["anion"],
    },
    {
        "name": "Chloride",
        "formula": "Cl{-}",
        "state": "aq",
        "charge": -1,
        "species_type": ["anion"],
    },
    {
        "name": "Nitrate",
        "formula": "NO3{-}",
        "state": "aq",
        "charge": -1,
        "species_type": ["anion"],
    },
    {
        "name": "Carbonate",
        "formula": "CO3{2-}",
        "state": "aq",
        "charge": -2,
        "species_type": ["anion"],
    },
    {
        "name": "Phosphate",
        "formula": "PO4{3-}",
        "state": "aq",
        "charge": -3,
        "species_type": ["anion"],
    },
    {
        "name": "Ferricyanide",
        "formula": "Fe(CN)6{3-}",
        "state": "aq",
        "charge": -3,
        "species_type": ["anion"],
    },
    {
        "name": "Bromide",
        "formula": "Br{-}",
        "state": "aq",
        "charge": -1,
        "species_type": ["anion"],
    },
    {
        "name": "Methyl radical",
        "formula": "CH3{*}",
        "state": "g",
        "charge": 0,
        "species_type": ["neutral", "radical"],
    },
    {
        "name": "Hydroxyl radical",
        "formula": "HO{*}",
        "state": "g",
        "charge": 0,
        "species_type": ["neutral", "radical"],
    },
    {
        "name": "Ethyl radical",
        "formula": "C2H5{*}",
        "state": "g",
        "charge": 0,
        "species_type": ["neutral", "radical"],
    },
    {
        "name": "Nitric oxide radical",
        "formula": "NO{*}",
        "state": "g",
        "charge": 0,
        "species_type": ["neutral", "radical"],
    },
    {
        "name": "Methyl radical cation",
        "formula": "CH3{*+}",
        "state": "g",
        "charge": 1,
        "species_type": ["cation", "radical"],
    },
    {
        "name": "Superoxide radical anion",
        "formula": "O2{*-}",
        "state": "aq",
        "charge": -1,
        "species_type": ["anion", "radical"],
    },
    {
        "name": "Benzene radical cation",
        "formula": "C6H6{*+}",
        "state": "g",
        "charge": 1,
        "species_type": ["cation", "radical"],
    },
    {
        "name": "Naphthalene radical anion",
        "formula": "C10H8{*-}",
        "state": "g",
        "charge": -1,
        "species_type": ["anion", "radical"],
    },
    {
        "name": "Radical dication",
        "formula": "C6H6{*2+}",
        "state": "g",
        "charge": 2,
        "species_type": ["cation", "radical"],
    },
    {
        "name": "Radical trication",
        "formula": "M{*3+}",
        "state": "s",
        "charge": 3,
        "species_type": ["cation", "radical"],
    },
    {
        "name": "Radical dianion",
        "formula": "A{*2-}",
        "state": "s",
        "charge": -2,
        "species_type": ["anion", "radical"],
    },
    {
        "name": "Radical tetracation",
        "formula": "M{*4+}",
        "state": "s",
        "charge": 4,
        "species_type": ["cation", "radical"],
    },
    {
        "name": "Radical pentacation",
        "formula": "M{*5+}",
        "state": "s",
        "charge": 5,
        "species_type": ["cation", "radical"],
    },
    {
        "name": "Radical trianion",
        "formula": "A{*3-}",
        "state": "s",
        "charge": -3,
        "species_type": ["anion", "radical"],
    },
    {
        "name": "Radical tetraanion",
        "formula": "A{*4-}",
        "state": "s",
        "charge": -4,
        "species_type": ["anion", "radical"],
    },
    {
        "name": "Peroxide radical dianion",
        "formula": "O2{*2-}",
        "state": "aq",
        "charge": -2,
        "species_type": ["anion", "radical"],
    },
    {
        "name": "Metal radical dication",
        "formula": "Fe{*2+}",
        "state": "aq",
        "charge": 2,
        "species_type": ["cation", "radical"],
    },
    {
        "name": "Glycine zwitterion",
        "formula": "NH3{+}-CH2-COO{-}",
        "state": "s",
        "charge": 0,
        "species_type": ["zwitterion"],
    },
    {
        "name": "Alanine zwitterion",
        "formula": "NH3{+}-CH(CH3)-COO{-}",
        "state": "s",
        "charge": 0,
        "species_type": ["zwitterion"],
    },
    {
        "name": "Betaine zwitterion",
        "formula": "N(CH3)3{+}-CH2-COO{-}",
        "state": "s",
        "charge": 0,
        "species_type": ["zwitterion"],
    },
    {
        "name": "Aspartate dianion",
        "formula": "OOC{-}-CH2-CH(NH2)-COO{-}",
        "state": "aq",
        "charge": -2,
        "species_type": ["anion"],
    },
    {
        "name": "Net neutral mixed centers",
        "formula": "M{2+}-L{-}-L{-}",
        "state": "s",
        "charge": 0,
        "species_type": ["zwitterion"],
    },
    {
        "name": "Net dianion with mixed centers",
        "formula": "M{2+}-L{2-}-L{2-}",
        "state": "s",
        "charge": -2,
        "species_type": ["anion"],
    },
    {
        "name": "Net cation with mixed charge centers",
        "formula": "NH3{+}-CH2-NH3{+}-COO{-}",
        "state": "aq",
        "charge": 1,
        "species_type": ["cation"],
    },
    {
        "name": "Net dication with mixed centers",
        "formula": "M{3+}-L{-}",
        "state": "s",
        "charge": 2,
        "species_type": ["cation"],
    },
    {
        "name": "Radical zwitterion",
        "formula": "N{+}-O{-}-C{*}",
        "state": "s",
        "charge": 0,
        "species_type": ["zwitterion", "radical"],
    },
    {
        "name": "Radical net cation mixed centers",
        "formula": "N{+}-O{-}-C{*+}",
        "state": "s",
        "charge": 1,
        "species_type": ["cation", "radical"],
    },
    {
        "name": "Radical net dication mixed centers",
        "formula": "M{2+}-L{-}-R{*+}",
        "state": "s",
        "charge": 2,
        "species_type": ["cation", "radical"],
    },
    {
        "name": "Radical net trication mixed centers",
        "formula": "M{3+}-L{-}-R{*+}",
        "state": "s",
        "charge": 3,
        "species_type": ["cation", "radical"],
    },
    {
        "name": "Radical net dianion mixed centers",
        "formula": "M{+}-L{2-}-R{*-}",
        "state": "s",
        "charge": -2,
        "species_type": ["anion", "radical"],
    },
    {
        "name": "Radical net trianion mixed centers",
        "formula": "M{+}-L{3-}-R{*-}",
        "state": "s",
        "charge": -3,
        "species_type": ["anion", "radical"],
    },
]


def check_component(case: dict) -> tuple[Component, bool]:
    component = Component(
        name=case["name"],
        formula=case["formula"],
        state=case["state"],
    )

    charge_ok = component.charge == case["charge"]
    species_ok = component.species_type == case["species_type"]

    assert charge_ok, (
        f"{component.formula}: expected charge {case['charge']}, "
        f"got {component.charge}"
    )
    assert species_ok, (
        f"{component.formula}: expected species_type {case['species_type']}, "
        f"got {component.species_type}"
    )

    explicit = Component(
        name=case["name"],
        formula=case["formula"],
        state=case["state"],
        charge=case["charge"],
    )
    assert explicit.charge == case["charge"]

    return component, charge_ok and species_ok


def render_table(rows: list[dict]) -> None:
    headers = [
        "Name",
        "Formula",
        "State",
        "Expected",
        "Actual",
        "Species Type",
        "Status",
    ]
    table = [
        [
            row["name"],
            row["formula"],
            row["state"],
            str(row["expected_charge"]),
            str(row["actual_charge"]),
            ", ".join(row["species_type"]),
            row["status"],
        ]
        for row in rows
    ]
    widths = [
        max(len(str(value)) for value in column)
        for column in zip(headers, *table)
    ]

    def line(values: list[str]) -> str:
        cells = [
            f" {value:<{widths[index]}} "
            for index, value in enumerate(values)
        ]
        return "|" + "|".join(cells) + "|"

    separator = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

    print(separator)
    print(line(headers))
    print(separator)
    for row in table:
        print(line(row))
    print(separator)


def check_inconsistent_charge() -> None:
    try:
        Component(
            name="Methyl radical cation",
            formula="CH3{*+}",
            state="g",
            charge=0,
        )
    except ValueError as exc:
        assert "inconsistent" in str(exc)
        return

    raise AssertionError("Expected inconsistent charge validation error.")


if __name__ == "__main__":
    start = time.perf_counter()
    rows = []

    for item in CASES:
        comp, ok = check_component(item)
        rows.append(
            {
                "name": comp.name,
                "formula": comp.formula,
                "state": comp.state,
                "expected_charge": item["charge"],
                "actual_charge": comp.charge,
                "species_type": comp.species_type,
                "status": "PASS" if ok else "FAIL",
            }
        )

    check_inconsistent_charge()
    elapsed = time.perf_counter() - start

    render_table(rows)
    print(f"Validated {len(CASES)} diverse component formulas.")
    print(f"Elapsed: {elapsed * 1000:.3f} ms")
