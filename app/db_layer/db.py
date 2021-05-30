# -----------------------------------------------------------
# handles all the database operations.
# author: Mohit
# -----------------------------------------------------------

import boto3
from boto3.dynamodb.conditions import Key
from db_layer import constants as const


# get the dynamodb client and table
def __get_table_client():
    client = boto3.resource('dynamodb')
    table = client.Table(const.TABLE_NAME)
    return table


# create a dynamodb table
def create_table():
    dynamodb = boto3.client('dynamodb')
    try:
        table = dynamodb.create_table(
            TableName=const.TABLE_NAME,
            KeySchema=[
                {
                    'AttributeName': const.PARTITION_KEY,
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': const.SORT_KEY,
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': const.PARTITION_KEY,
                    'AttributeType': 'S'
                },
                {
                    'AttributeName': const.SORT_KEY,
                    'AttributeType': 'S'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        print("Table is created")
    except dynamodb.exceptions.ResourceInUseException:
        print("Table already in use")


# insert repo details into table
def repo_insert(repo_obj):
    table = __get_table_client()
    try:
        response = table.put_item(
            Item={
                const.PARTITION_KEY: repo_obj.owner,
                const.SORT_KEY: repo_obj.name,
                const.ATTR_STEPS_NAME: repo_obj.steps,
                const.ATTR_COMPLAINT_STATUS: repo_obj.status,
                const.ATTR_MISSING_STEPS: repo_obj.req_steps
            }
        )
        print("item inserted {}".format(response))
    except table.exceptions as error:
        print(error)


# get details of particular repo under organization
def get_repo_details(org_name, repo_name):
    table = __get_table_client()
    try:
        response = table.get_item(
            Key={
                const.PARTITION_KEY: org_name,
                const.SORT_KEY: repo_name
            }
        )
        return response
    except table.exceptions.ResourceNotFoundException as e:
        return e


# get details of all repos present under organization
def query_org_repo(org_name):
    table = __get_table_client()
    try:
        response = table.query(
            KeyConditionExpression=Key(const.PARTITION_KEY).eq(org_name)
        )
        return response['Items']
    except table.exceptions.ResourceNotFoundException as e:
        return e
