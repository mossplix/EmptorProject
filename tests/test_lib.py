#!/usr/bin/env python3
from urllib.parse import urlparse
import pytest
from trialproject.lib import InvalidUrlException, validate_url


def test_validate_url():
    """invalid url should raise InvalidUrlException"""
    url = "http://googlecom"

    with pytest.raises(InvalidUrlException):
        res = validate_url(url)
