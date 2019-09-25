#!/usr/bin/env python3
import pytest
import uuid
import os
import mock
from trialproject.lib import InvalidUrlException, validate_url,\
    get_title, fetch_url, get_s3object_url, s3bucket_put, DynamoRepository,\
    send_sqs_message, process_url


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


def mock_fetch_url(*args, **kwargs):
    return """
    <html><head><title>Google</title>
    </head></html>

    """


@mock.patch('trialproject.lib.fetch_url', side_effect=mock_fetch_url)
def test_fetch_url(mock_fetch_url):
    """test url fetching"""

    valid_url = "https://www.google.com"

    res = fetch_url(valid_url)

    assert b"google" in res


def mock_s3_put(*args, **kwargs):
    return True


def mock_send_sqs_message(*args, **kwargs):
    return True


@mock.patch('trialproject.lib.s3bucket_put', side_effect=mock_s3_put)
def test_bucket_put_and_get(mock_s3_put):
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


@mock.patch('trialproject.lib.send_sqs_message',
            side_effect=mock_send_sqs_message)
def test_send_sqs_message(mock_send_sqs_message):

    res = send_sqs_message("test")
    assert res is not None


def test_process_url():
    valid_url = "https://www.google.com"

    res = process_url(valid_url)
    assert res is not None
