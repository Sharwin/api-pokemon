import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'pokemon'))

def handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        required = ['id', 'name', 'height', 'weight', 'types']
        if not all(k in body for k in required):
            return {'statusCode': 400, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Missing required fields'})}
        table.put_item(Item=body)
        return {'statusCode': 201, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(body)}
    except json.JSONDecodeError:
        return {'statusCode': 400, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Invalid JSON'})}
    except Exception:
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Internal server error'})}
