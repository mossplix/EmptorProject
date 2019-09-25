#!/usr/bin/env python3
import pytest
import uuid
import os
from trialproject.lib import InvalidUrlException, validate_url,\
    get_title, fetch_url, get_s3object_url, s3bucket_put, DynamoRepository


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


def test_bucket_put_and_get():
    """
      test s3 operations
    """
    key = str(uuid.uuid4())
    bucket = os.environ.get('s3_bucket')
    item = ""
    assert bucket is not None
    response1 = s3bucket_put(key, item, bucket)
    assert response1 is not None

    response2 = get_s3object_url(key, bucket)
    assert response2 is not None


def test_dynamo_repository():
    """
      smoke test dynamo repossitory
    """
    repo = DynamoRepository("foo")
    assert repo is not None
