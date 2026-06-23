def calculate_percentage_change(current: int | float, previous: int | float) -> float:
    """
    Calculate the percentage change between two numbers.

    Args:
        current (int | float): The current value.
        previous (int | float): The previous value.

    Returns:
        float | None: The percentage change from previous to current, or None if previous is zero.
    """
    if previous == 0:
        return 100.0 if current > 0 else 0.0
    
    change = current - previous
    percentage_change = round((change / previous) * 100, 2)
    return percentage_change