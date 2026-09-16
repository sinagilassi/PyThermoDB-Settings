# import libs
from pythermodb_settings.utils import measure_time, timed
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


@timed
def fibonacci_timed(n: int, **kwargs) -> int:
    """Calculate the n-th Fibonacci number."""
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


# ! calculate the 10th Fibonacci number
# >> mode: silent
result = fibonacci(20, mode="silent")
print(result)

# >> mode: log
result = fibonacci(20, mode="log")
print(result)

# >> mode: attach
result = fibonacci(20, mode="attach")
print(result)

# ! ::: fibonacci_timed function
result = fibonacci_timed(20, mode="silent")
print(result)

result = fibonacci_timed(20, mode="log")
print(result)

result = fibonacci_timed(20, mode="attach")
print(result)
