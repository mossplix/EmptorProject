#!/usr/bin/env python3

from urllib.parse import urlparse
from bs4 import BeautifulSoup
import boto3
import json
import uuid
import requests
import os
from botocore.exceptions import ClientError

from boto3.dynamodb.conditions import Key, Attr
from boto3 import resource


class InvalidUrlException(Exception):
    "returned when the url is invalid"
    pass


class DynamoRepository:
    def __init__(self, table_name):
        self.client = resource('dynamodb')
        self.table_name = table_name
        self.table = self.client.Table(table_name)

    def query_by_key(self, key):
        response = self.table.query(
            KeyConditionExpression=Key("id").eq(key))
        [toret] = response.get('Items')
        return toret

    def put_item(self, key, title="None", url="None", s3Url="None", state="PENDING"):

        try:
            response = self.table.put_item(
                Item={'id': key,
                      'title': title,
                      'url': url,
                      's3Url': s3Url,
                      'state': state
                      }
            )
        except ClientError as e:
            print("Unexpected error: %s" % e)


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


def get_s3object_url(key, bucket):
    return 'https://%s.s3.amazonaws.com/%s' % (bucket, key)


def s3bucket_put(key, item, bucket):
    s3_client = boto3.client('s3')
    if isinstance(item, str):
        item = item.encode()
    try:
        s3_client.put_object(Body=item, Bucket=bucket, Key=key)
    except ClientError as e:
        if e.response['Error']['Code'] == 'EntityAlreadyExists':
            print("item already exists")
        else:
            print("Unexpected error: %s" % e)
    return True


def get_key():
    return str(uuid.uuid4())


def send_sqs_message(message):
    client = boto3.client('sqs')
    sqsAddress = client.get_queue_url(QueueName='WriteSQS')
    msgUrl = sqsAddress['QueueUrl']
    response = client.send_message(
        QueueUrl=msgUrl, MessageBody=message)

    return response


def process_url(url):
    content = fetch_url(url)
    bucket = os.environ.get('s3_bucket')
    key = get_key()
    title = get_title(content)
    s3bucket_put(key, title, bucket)
    return {"title": title, "s3url": get_s3object_url(bucket, key), "state": "PROCESSED"}
