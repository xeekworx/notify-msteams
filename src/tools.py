from urllib.parse import urlparse


def is_valid_url(url: str):
    """
    Check if the given string is a valid URL.

    This function uses urlparse to parse the URL and then checks if it has both a scheme (like http, https) 
    and a netloc (domain name). If both are present and valid, the URL is considered valid.

    Args:
    url (str): The URL string to validate.

    Returns:
    bool: True if the string is a valid URL, False otherwise.
    """
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def is_hex(s: str):
    """
    Check if the provided string is a valid hexadecimal value.

    The function tries to convert the string to an integer with base 16. If the conversion is successful, 
    the string is a valid hexadecimal. Otherwise, it's not a valid hex value.

    Args:
    s (str): The string to check for hexadecimal validity.

    Returns:
    bool: True if the string is a valid hexadecimal, False otherwise.
    """
    try:
        int(s.lstrip("#"), 16)
        return True
    except ValueError:
        return False
