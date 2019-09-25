#!/usr/bin/env python3


from .lib import validate_url, fetch_url, get_title


def handle_url(event, context):

    url = validate_url(event)
    content = fetch_url(url)
    title = get_title(content)
    response = {
        "statusCode": 200,
        "body": title
    }

    return response
