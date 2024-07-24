import re


def verify_email_pattern(value):
    emailRegex = re.compile(
    r'[a-zA-Z0-9._%+-]+'
    r'@'
    r'[a-zA-Z0-9.-]+'
    r'\.[a-zA-Z]{2,4}'          
    , re.IGNORECASE)

    return re.match(emailRegex,value)


def verify_url_pattern(value):
    url_regex = re.compile(
        r'^(?:http|ftp)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$',re.IGNORECASE
    )

    return re.match(url_regex,value)