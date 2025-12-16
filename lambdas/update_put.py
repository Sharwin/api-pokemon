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
        body = json.loads(event.get('body', '{}'))
        update_parts = []
        expr_values = {}
        expr_names = {}
        for k, v in body.items():
            if k != 'id':
                update_parts.append(f'#{k} = :{k}')
                expr_values[f':{k}'] = v
                expr_names[f'#{k}'] = k
        if not expr_values:
            return {'statusCode': 400, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'No fields to update'})}
        update_expr = 'SET ' + ', '.join(update_parts)
        table.update_item(Key={'id': pokemon_id}, UpdateExpression=update_expr, ExpressionAttributeValues=expr_values, ExpressionAttributeNames=expr_names)
        return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'id': pokemon_id, **body})}
    except json.JSONDecodeError:
        return {'statusCode': 400, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Invalid JSON'})}
    except Exception:
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Internal server error'})}
