import re

def verify_email_pattern(value):
    """
    Verify if the given value matches the standard email pattern.

    This function uses a regular expression to check if the input string is a valid email address format.

    Args:
        value (str): The string to be checked.

    Returns:
        re.Match or None: Returns a match object if the value matches the email pattern, otherwise None.

    Example:
        >>> verify_email_pattern('user@example.com')
        <re.Match object; span=(0, 16), match='user@example.com'>
    """
    emailRegex = re.compile(
        r'[a-zA-Z0-9._%+-]+'
        r'@'
        r'[a-zA-Z0-9.-]+'
        r'\.[a-zA-Z]{2,4}',          
        re.IGNORECASE
    )

    return re.match(emailRegex, value)


def verify_url_pattern(value):
    """
    Verify if the given value matches the standard URL pattern.

    This function uses a regular expression to check if the input string is a valid URL format.

    Args:
        value (str): The string to be checked.

    Returns:
        re.Match or None: Returns a match object if the value matches the URL pattern, otherwise None.

    Example:
        >>> verify_url_pattern('https://www.example.com')
        <re.Match object; span=(0, 23), match='https://www.example.com'>
    """
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$',
        re.IGNORECASE
    )

    return re.match(url_regex, value)
