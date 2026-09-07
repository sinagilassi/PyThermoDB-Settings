# import libs
# from rich import print
from typing import Mapping
from pythermodb_settings.decorators.calculation_info import calculation_info, get_calculation_info, get_calculation_signature


@calculation_info(
    name="calc_ionic_strength_molality",
    description=(
        "Calculate molality-based ionic strength from species "
        "molalities and ionic charges."
    ),
    equation="I = 0.5 * sum(m_i * z_i^2)",
    inputs={
        "molalities": "Species molalities [mol/kg]",
        "charges": "Species ionic charge numbers [-]",
    },
    outputs={
        "ionic_strength": "Molality-based ionic strength [mol/kg]",
    },
    notes=(
        "Use true ionic species.",
        "All relevant charged species should be included.",
    ),
    aliases=(
        "calc_ionic_strength",
    ),
    tags=(
        "ionic_strength",
        "molality",
    )
)
def calc_ionic_strength_molality(
    molalities: Mapping[str, float],
    charges: Mapping[str, int],
) -> float:
    return 0.5 * sum(
        molalities[component] * charges[component] ** 2
        for component in molalities
    )


info = \
    calc_ionic_strength_molality.__calculation_info__  # type: ignore[attr-defined]
print(info)

print(info.name)
print(info.description)
print(info.equation)
print(info.inputs)
print(info.outputs)
print(info.notes)
print(info.aliases)
print(info.tags)

sig = get_calculation_signature(calc_ionic_strength_molality)

print(sig.parameters)
print(sig.return_type)
