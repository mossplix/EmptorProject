"""Test index file"""

import pytest
from trialproject.index import handle_url


def test_handle_url_args():
    """handle url should take take 2 arguments"""

    with pytest.raises(TypeError):
        res = handle_url()


def test_handle_url_invalid_url():
    """handle url should take a valid url"""

    with pytest.raises(TypeError):
        res = handle_url()
