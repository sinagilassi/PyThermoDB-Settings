# import libs
from rich import print
from pythermodb_settings.decorators import annotated_value
from pythermodb_settings.models import AnnotatedValue
from typing import Any

# NOTE: sample usage of the annotated_value decorator


@annotated_value
def calculate_x(
        x: float,
        y: float,
        *,
        name: str = "power function",
        unit: str = "dimensionless",
        description: str = "calculation of x",
        symbol: str = "x",
) -> float:
    res = x**y
    return res


# execute
res: AnnotatedValue[float] = calculate_x(2, 3)
print(res)
