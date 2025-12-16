import json
import os
import boto3
from decimal import Decimal

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super().default(obj)

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'pokemon'))

def handler(event, context):
    try:
        pokemon_id = event['pathParameters']['id']
        response = table.get_item(Key={'id': pokemon_id})
        if 'Item' not in response:
            return {'statusCode': 404, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Not found'})}
        return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps(response['Item'], cls=DecimalEncoder)}
    except Exception:
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Internal server error'})}
