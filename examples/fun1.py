# import libs
from pythermodb_settings.utils import measure_time
from rich import print

# NOTE: fibonacci function


@measure_time
def fibonacci(n: int, **kwargs) -> int:
    """Calculate the n-th Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# calculate the 10th Fibonacci number
# >> mode: silent
result = fibonacci(10, mode="silent")
print(result)

# >> mode: log
result = fibonacci(10, mode="log")
print(result)

# >> mode: attach
result = fibonacci(10, mode="attach")
print(result)
