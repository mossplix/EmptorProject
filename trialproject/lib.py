#!/usr/bin/env python3

from urllib.parse import urlparse


class InvalidUrlException(Exception):
    "returned when the url is invalid"
    pass


def validate_url(url):
    """validate url"""
    try:
        result = urlparse(url)
        is_valid = all([result.scheme, result.netloc, result.path])
    except AttributeError:
        is_valid = False

    if is_valid:
        return url
    else:
        raise InvalidUrlException("The Url Is Malformed")
