#!/usr/bin/env python3

import json
from .lib import validate_url


def handle_url(event, context):

    url = validate_url(event)

    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response
