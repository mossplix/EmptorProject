#!/usr/bin/env python3
import pytest
from trialproject.lib import InvalidUrlException, validate_url,\
    get_title, fetch_url


def test_validate_url():
    """invalid url should raise InvalidUrlException"""
    invalid_url = "http:/googlecom"

    with pytest.raises(InvalidUrlException):
        validate_url(invalid_url)

    valid_url = "https://www.google.com"
    assert valid_url == validate_url(valid_url)


def test_get_title():
    """ test extracting of title  from doc"""
    doc = """ <html><head><title>Hello World</title>
    </head></html>"""
    res = get_title(doc)
    assert res == "Hello World"


def test_fetch_url():
    """test url fetching"""

    valid_url = "https://www.google.com"

    res = fetch_url(valid_url)

    assert b"google" in res
