#!/usr/bin/env python3
import os

from .lib import validate_url, get_key, DynamoRepository,\
    send_sqs_message, process_url

import logging
import boto3
logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handle_url(event, context):
    table_name = os.environ.get('dynamo_table')
    repo = DynamoRepository(table_name)
    if isinstance(event, str):
        key = get_key()
        url = validate_url(event)
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
                if record["eventName"] == "INSERT":
                    item = record["dynamodb"]["NewImage"]
                    logger.info('processing item: %s', item)

                    url = item["url"]["S"]

                    res = process_url(url)

                    repo.put_item(item["id"]["S"], res["title"],
                                  url, res["s3url"], "PROCESSED")
                elif record.get("body"):
                    payload = record["body"]

                    logger.info('processing record: %s', payload)
                    item = repo.query_by_key(payload)
                    res = process_url(item["url"])

                    repo.put_item(item["id"], res["title"],
                                  item["url"], res["s3url"], "PROCESSED")

                    client = boto3.client('sqs')
                    sqsAddress = client.get_queue_url(QueueName='WriteSQS')

                    msgUrl = sqsAddress['QueueUrl']

                    client.delete_message(
                        QueueUrl=msgUrl,
                        ReceiptHandle=record["receiptHandle"])


def queryByKey(key):
    """
     query dynamo table by key
    """
    table_name = os.environ.get('dynamo_table')
    repo = DynamoRepository(table_name)
    return repo.query_by_key(key)
