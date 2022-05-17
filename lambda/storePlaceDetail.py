import json
import boto3
import datetime
from dynamodb_json import json_util as ddjson
from boto3.dynamodb.conditions import Key
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
import copy


def put_user_search_activity_into_dynamodb(user_id, place_id):
    session = boto3.Session()
    ddb = session.client("dynamodb")
    table = "user_activity"

    curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    item = dict()
    item["event_date_time"] = {"N": curr_dt}
    item["event_type"] = {"S": "click"}
    item["place_ids"] = {"L": [{"S": place_id}]}
    item["username"] = {"S": user_id}
    item["activity_id"] = {"S": f"{user_id}_{curr_dt}"}

    response = ddb.put_item(TableName=table, Item=item)
    print(f"response from dynamodb after putting user activity: {response}")


def put_places_data_into_dynamodb(place, place_id):
    session = boto3.Session()
    ddb = session.client("dynamodb")
    table = "places"
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    dyndb = dynamodb.Table('places')
    srch_cnt = intrsted_cnt = clicked_cnt = 0

    check_item = dyndb.query(KeyConditionExpression=Key('place_id').eq(str(place_id)))

    if len(check_item["Items"]) > 0:
        print(f"place_id: {place_id} ALREADY found in DynamoDB: {check_item['Items']}")
        upd_item = check_item["Items"][0]
        srch_cnt = upd_item["search_count"]
        clicked_cnt = upd_item["clicked_count"]
        intrsted_cnt = upd_item["interested_count"]

    print("Place: ")
    print(place)
    place["place_id"] = place_id
    place["search_count"] = srch_cnt
    place["interested_count"] = intrsted_cnt
    place["clicked_count"] = clicked_cnt + 1
    open_status = place.get("opening_hours", {}).get("open_now", None)
    if open_status is not None:
        if str(open_status).lower() == "true":
            open_status = True
        elif str(open_status).lower() == "false":
            open_status = False
        place["opening_hours"]["open_now"] = open_status
    upd_item = ddjson.dumps(place)
    print(f"dynamo db jsonified item: {upd_item}")
    response = ddb.put_item(TableName=table, Item=json.loads(upd_item))
    print(f"response from dynamodb: {response}")


def lambda_handler(event, context):
    # TODO implement

    username = event["user_name"]
    place_id = event["place_id"]
    place_data = event["place_data"]

    put_user_search_activity_into_dynamodb(username, place_id)
    put_places_data_into_dynamodb(copy.copy(place_data), place_id)

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
