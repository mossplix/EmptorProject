#!/usr/bin/env python3

from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests


class InvalidUrlException(Exception):
    "returned when the url is invalid"
    pass


def get_title(html):
    body = BeautifulSoup(html, "lxml")
    title = body.find("title").text
    return title


def validate_url(url):
    """validate url"""
    try:
        result = urlparse(url)
        is_valid = all([result.scheme, result.netloc])
    except (AttributeError, ValueError):
        is_valid = False

    if is_valid:
        return url
    else:
        raise InvalidUrlException("The Url Is Malformed")


def fetch_url(url):
    """ fetch url and return html content"""

    with requests.Session() as session:
        response = session.get(
            url, verify=False)
        return response.content
