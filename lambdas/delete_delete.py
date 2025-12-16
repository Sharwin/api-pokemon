import json
import os
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ.get('TABLE_NAME', 'pokemon'))

def handler(event, context):
    try:
        pokemon_id = event['pathParameters']['id']
        table.delete_item(Key={'id': pokemon_id})
        return {'statusCode': 200, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'message': 'Deleted'})}
    except Exception:
        return {'statusCode': 500, 'headers': {'Content-Type': 'application/json'}, 'body': json.dumps({'error': 'Internal server error'})}
