def logger(func):
    """
    A decorator function that logs the start and end of the execution of the decorated function.

    Parameters:
    func (function): The function to be decorated.

    Returns:
    function: The wrapped function with logging capabilities.
    """
    def wrapper(*args, **kwargs):
        """
        Wrapper function that logs the start and end of the execution of the decorated function.

        Parameters:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

        Returns:
        The result of the decorated function.
        """
        print(f"Starting execution of function {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Finishing execution of function {func.__name__}")
        return result
    return wrapper


@logger
def calculate_ln_series(x, eps):
    """
    Calculates the natural logarithm of (1 + x) using a series expansion.

    Parameters:
    x (float): The value for which the natural logarithm is to be calculated. |x| must be less than 1.
    eps (float): The precision threshold for the series convergence.

    Returns:
    tuple: A tuple containing the number of iterations (n) and the sum of the series.

    Raises:
    ValueError: If |x| is greater than or equal to 1, which would cause the series to diverge.
    """
    if abs(x) >= 1:
        raise ValueError("Error: |x| must be less than 1 for the series to converge.")

    n = 1
    sum_series = 0.0
    max_iterations = 500
    previous_sum = 0.0

    while n <= max_iterations:
        term = -(x ** n) / n
        sum_series += term
        if abs(sum_series - previous_sum) < eps:
            break
        previous_sum = sum_series
        n += 1

    return n, sum_series