#!/usr/bin/env python3
import os
import uuid

from .lib import validate_url, fetch_url, get_title, \
    s3bucket_put, get_key, get_s3object_url, DynamoRepository,\
    send_sqs_message

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle_url(event, context):
    bucket = os.environ.get('s3_bucket')
    table_name = os.environ.get('dynamo_table')
    key = get_key()

    url = validate_url(event)
    content = fetch_url(url)
    title = get_title(content)

    send_sqs_message(key)

    repo = DynamoRepository(table_name)
    repo.put_item(key=key,
                  url=url, state="PENDING")

    response = {
        "statusCode": 200,
        "key": key
    }

    return response
