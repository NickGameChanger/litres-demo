from datetime import datetime, date


def string_to_datetime(string: str) -> datetime:
    # Example string in the format 'YYYY-MM-DD HH:MM:SS'
    try:
        date_format = '%Y-%m-%d %H:%M:%S'
        # Parse the string to a datetime object
        date_object = datetime.strptime(string, date_format)
        return date_object
    except Exception:
        raise ValueError('wrong data format')
