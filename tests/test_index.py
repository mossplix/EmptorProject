#!/usr/bin/env python3
"""Test index file"""

import pytest
import os
from trialproject.index import handle_url
from trialproject.lib import InvalidUrlException


def test_env_variables():
    """ make sure certain environment variables are set """
    assert os.environ.get('S3_BUCKET') is not None


def test_handle_url_args():
    """handle url should take take 2 arguments"""

    with pytest.raises(TypeError):
        handle_url()


def test_handle_url_invalid_url():
    """handle url should take a valid url"""

    with pytest.raises(InvalidUrlException):
        handle_url("", {})


def test_handle_url():
    valid_url = "https://www.google.com"
    invalid_url = ""
    valid_response = handle_url(valid_url, {})
    assert valid_response["body"] == "Google"

    with pytest.raises(InvalidUrlException):
        handle_url(invalid_url, {})
