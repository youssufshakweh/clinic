def fill_weekday_gaps(data: list[dict]) -> list[dict]:
    """
    Fill missing weekdays with zero values.
    
    Args:
        data: List of dicts with 'weekday' (0-6) and 'count' keys
        
    Returns:
        List of dicts with all 7 weekdays (0=Monday to 6=Sunday)
    """
    weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    data_dict = {item['weekday']: item['count'] for item in data}
    
    filled_data = []
    for weekday_id in range(7):
        filled_data.append({
            'weekday': weekday_id,
            'day_name': weekday_names[weekday_id],
            'count': data_dict.get(weekday_id, 0)
        })
    
    return filled_data


def fill_month_gaps(data: list[dict], year: int | None = None) -> list[dict]:
    """
    Fill missing months with zero values.
    
    Args:
        data: List of dicts with 'month' (1-12) and 'count' keys
        year: Optional year for month names
        
    Returns:
        List of dicts with all 12 months
    """
    month_names = [
        'January', 'February', 'March', 'April', 'May', 'June',
        'July', 'August', 'September', 'October', 'November', 'December'
    ]
    data_dict = {item['month']: item['count'] for item in data}
    
    filled_data = []
    for month_id in range(1, 13):
        filled_data.append({
            'month': month_id,
            'month_name': month_names[month_id - 1],
            'count': data_dict.get(month_id, 0)
        })
    
    return filled_data


def fill_year_gaps(data: list[dict], start_year: int | None = None, end_year: int | None = None) -> list[dict]:
    """
    Fill missing years with zero values.
    
    Args:
        data: List of dicts with 'year' and 'count' keys
        start_year: Optional start year for range
        end_year: Optional end year for range
        
    Returns:
        List of dicts with all years in the range
    """
    if not data:
        return []
    
    if start_year is None:
        start_year = min(item['year'] for item in data)
    if end_year is None:
        end_year = max(item['year'] for item in data)
    
    data_dict = {item['year']: item['count'] for item in data}
    
    filled_data = []
    for year in range(start_year, end_year + 1):
        filled_data.append({
            'year': year,
            'count': data_dict.get(year, 0)
        })
    
    return filled_data
