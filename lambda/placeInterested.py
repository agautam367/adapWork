import json
import datetime
import boto3
from dynamodb_json import json_util as ddjson
from boto3.dynamodb.conditions import Key


def put_user_interested_activity_in_dynamodb(username, place_id):
    session = boto3.Session()
    ddb = session.client("dynamodb")
    table = "user_activity"

    curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    item = dict()
    item["event_date_time"] = {"N": curr_dt}
    item["event_type"] = {"S": "interest"}
    item["place_ids"] = {"L": [{"S": place_id}]}
    item["username"] = {"S": username}
    item["activity_id"] = {"S": f"{username}_{curr_dt}"}

    response = ddb.put_item(TableName=table, Item=item)
    print(f"response from dynamodb after putting user activity: {response}")


def update_interest_count_in_places_ddb(place_id):
    session = boto3.Session()
    ddb = session.client("dynamodb")
    table = "places"
    ddob = boto3.resource('dynamodb', region_name='us-east-1')
    tableobj = ddob.Table(table)

    # check if the place is already present
    check_item = tableobj.query(KeyConditionExpression=Key('place_id').eq(str(place_id)))

    if len(check_item["Items"]) > 0:
        print(f"place_id: {place_id} ALREADY found in DynamoDB: {check_item['Items']}")
        upd_item = check_item["Items"][0]
        upd_item["interested_count"] += 1
        upd_item = ddjson.dumps(upd_item)

        print(f"dynamo db jsonified item: {upd_item}")
        response = ddb.put_item(TableName=table, Item=json.loads(upd_item))
        print(f"response from dynamodb: {response}")
    else:
        print(f"place_id: {place_id} NOT found in DynamoDB: {check_item['Items']}")


def clean_params(params):
    upd_params = dict()
    for param, value in params.items():
        if value is not None and value.lower() != "none" and value.lower() != "undefined" and value != "null":
            upd_params[param] = value
    return upd_params


def lambda_handler(event, context):
    # TODO implement
    print(f"event: {event}")

    # ToDo: event object MUST contain all the below REQUIRED and OPTIONAL params
    params = event.get("queryStringParameters")
    if not params:
        params = dict()
    params = clean_params(params)

    place_id = params.get(" placeId", "ChIJN1t_tDeuEmsRUsoyG83frY4")
    username = params.get("username", "foo")

    # put user search activity into "user_activity" dynamo db
    put_user_interested_activity_in_dynamodb(username, place_id)

    # update interested count in places dynamodb
    update_interest_count_in_places_ddb(place_id)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
