#!/usr/bin/env python3
import os
import uuid
import json

from .lib import validate_url, fetch_url, get_title, \
    s3bucket_put, get_key, get_s3object_url, DynamoRepository,\
    send_sqs_message, process_url

import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle_url(event, context):
    table_name = os.environ.get('dynamo_table')
    repo = DynamoRepository(table_name)
    if isinstance(event, str):
        key = get_key()

        url = validate_url(event)
        content = fetch_url(url)
        title = get_title(content)

        send_sqs_message(key)
        repo.put_item(key=key,
                      url=url, state="PENDING")

        response = {
            "statusCode": 200,
            "key": key
        }

        return response
    elif isinstance(event, dict):
        if event.get("Records"):
            for record in event['Records']:
                payload = record["body"]

                logger.info('processing record: %s', payload)
                item = repo.query_by_key(payload)
                res = process_url(item["url"])

                repo.put_item(item["id"], res["title"],
                              item["url"], res["s3url"], "PROCESSED")

                client = boto3.client('sqs')
                sqsAddress = client.get_queue_url(QueueName='WriteSQS')

                msgUrl = sqsAddress['QueueUrl']

                client.delete_message(QueueUrl=msgUrl,
                                      ReceiptHandle=record["receiptHandle"])
