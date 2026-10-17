"""
Visitor counter Lambda for vishnurachapudi.com.

Flow: API Gateway (HTTP API, GET /count) -> this Lambda -> DynamoDB atomic increment.
Returns JSON: {"count": <int>}

Environment variables:
  TABLE_NAME   DynamoDB table name (default: visitor-counter)
  ITEM_ID      Partition key value of the single counter item (default: site)
  ALLOW_ORIGIN CORS origin to allow (default: https://www.vishnurachapudi.com)
"""

import json
import os

import boto3

TABLE_NAME = os.environ.get("TABLE_NAME", "visitor-counter")
ITEM_ID = os.environ.get("ITEM_ID", "site")
ALLOW_ORIGIN = os.environ.get("ALLOW_ORIGIN", "https://www.vishnurachapudi.com")

_dynamodb = boto3.resource("dynamodb")
_table = _dynamodb.Table(TABLE_NAME)


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": ALLOW_ORIGIN,
            "Access-Control-Allow-Methods": "GET,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
            "Cache-Control": "no-store",
        },
        "body": json.dumps(body),
    }


def handler(event, context):
    # Handle CORS preflight if it ever reaches the function.
    method = (
        event.get("requestContext", {})
        .get("http", {})
        .get("method", "GET")
    )
    if method == "OPTIONS":
        return _response(204, {})

    try:
        result = _table.update_item(
            Key={"id": ITEM_ID},
            UpdateExpression="ADD visits :inc",
            ExpressionAttributeValues={":inc": 1},
            ReturnValues="UPDATED_NEW",
        )
        count = int(result["Attributes"]["visits"])
        return _response(200, {"count": count})
    except Exception as exc:  # noqa: BLE001 - surface a clean error to the client
        print(f"visitor-counter error: {exc}")
        return _response(500, {"error": "counter_unavailable"})
