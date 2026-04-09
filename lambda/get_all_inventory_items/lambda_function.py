import boto3
import json
import os
from boto3.dynamodb.types import TypeDeserializer

def lambda_handler(event, context):
    # Initialize DynamoDB client
    dynamo_client = boto3.client('dynamodb')

    # Get table name from environment variable
    table_name = os.getenv('TABLE_NAME', 'Inventory')

    # Deserializer for DynamoDB types
    deserializer = TypeDeserializer()

    def deserialize_item(item):
        return {key: deserializer.deserialize(value) for key, value in item.items()}

    # Scan the table
    try:
        response = dynamo_client.scan(TableName=table_name)
        items = [deserialize_item(item) for item in response['Items']]

        return {
            'statusCode': 200,
            'body': json.dumps(items, default=str)
        }
    except Exception as e:
        print(e)
        return {
            'statusCode': 500,
            'body': json.dumps(str(e))
        }