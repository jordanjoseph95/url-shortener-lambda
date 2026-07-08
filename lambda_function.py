import json
import random
import string
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("url-shortener")

def generate_short_code(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(random.choices(characters, k=length))

def lambda_handler(event, context):
    http_method = event.get("requestContext", {}).get("http", {}).get("method")

    if http_method == "POST":
        body = json.loads(event.get("body", "{}"))
        long_url = body.get("url")

        if not long_url:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing 'url' in request body"})
            }

        short_code = generate_short_code()

        table.put_item(Item={
            "short_code": short_code,
            "long_url": long_url
        })

        return {
            "statusCode": 200,
            "body": json.dumps({"short_code": short_code})
        }

    elif http_method == "GET":
        short_code = event.get("pathParameters", {}).get("code")

        if not short_code:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Missing short code"})
            }

        response = table.get_item(Key={"short_code": short_code})
        item = response.get("Item")

        if not item:
            return {
                "statusCode": 404,
                "body": json.dumps({"error": "Short code not found"})
            }

        return {
            "statusCode": 302,
            "headers": {"Location": item["long_url"]},
            "body": ""
        }

    return {
        "statusCode": 405,
        "body": json.dumps({"error": "Method not allowed"})
    }
