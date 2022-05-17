import json
import boto3
from google_api import places_api
import datetime
from dynamodb_json import json_util as ddjson
from opensearchpy import OpenSearch, RequestsHttpConnection
from boto3.dynamodb.conditions import Key
from requests_aws4auth import AWS4Auth
import copy

# Google API Personal Key (Manish)
GOOGLE_KEY = "AIzaSyDAEnmrfeFCXgLgOa_gWKfq5XKrOYs_GBs"


# def put_user_search_activity_into_dynamodb(user_id, place_id):
#     session = boto3.Session()
#     ddb = session.client("dynamodb")
#     table = "user_activity"

#     curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     item = dict()
#     item["event_date_time"] = {"N": curr_dt}
#     item["event_type"] = {"S": "click"}
#     item["place_ids"] = {"L": [{"S": place_id}]}
#     item["username"] = {"S": user_id}
#     item["activity_id"] = {"S": f"{user_id}_{curr_dt}"}

#     response = ddb.put_item(TableName=table, Item=item)
#     print(f"response from dynamodb after putting user activity: {response}")


# def put_places_data_into_dynamodb(place, place_id):
#     session = boto3.Session()
#     ddb = session.client("dynamodb")
#     table = "places"
#     dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
#     dyndb = dynamodb.Table('places')
#     srch_cnt = intrsted_cnt = clicked_cnt = 0

#     check_item = dyndb.query(KeyConditionExpression=Key('place_id').eq(str(place_id)))

#     if len(check_item["Items"]) > 0:
#         print(f"place_id: {place_id} ALREADY found in DynamoDB: {check_item['Items']}")
#         upd_item = check_item["Items"][0]
#         srch_cnt = upd_item["search_count"]
#         clicked_cnt = upd_item["clicked_count"]
#         intrsted_cnt = upd_item["interested_count"]

#     print("Place: ")
#     print(place)
#     place["place_id"] = place_id
#     place["search_count"] = srch_cnt
#     place["interested_count"] = intrsted_cnt
#     place["clicked_count"] = clicked_cnt + 1
#     open_status = place.get("opening_hours", {}).get("open_now", None)
#     if open_status is not None:
#         if str(open_status).lower() == "true":
#             open_status = True
#         elif str(open_status).lower() == "false":
#             open_status = False
#         place["opening_hours"]["open_now"] = open_status
#     upd_item = ddjson.dumps(place)
#     print(f"dynamo db jsonified item: {upd_item}")
#     response = ddb.put_item(TableName=table, Item=json.loads(upd_item))
#     print(f"response from dynamodb: {response}")


def store_user_activity_and_places_data_into_os_db(username, place_id, place_data):
    client = boto3.client('lambda')

    input_params = dict()
    input_params["user_name"] = username
    input_params["place_id"] = place_id
    input_params["place_data"] = place_data

    client.invoke(
        FunctionName="arn:aws:lambda:us-east-1:992229545431:function:storePlaceDetail",
        InvocationType='Event',
        Payload=json.dumps(input_params)
    )


def get_live_forecast(name, address):
    client = boto3.client('lambda')

    print(f"name: {name}, address: {address}")

    input_params = dict()
    input_params["venue_name"] = name
    input_params["venue_address"] = address

    response = client.invoke(
        FunctionName="arn:aws:lambda:us-east-1:992229545431:function:placeLiveForecast",
        InvocationType='RequestResponse',
        Payload=json.dumps(input_params)
    )
    response = json.load(response['Payload'])
    print(f"response from live forecast api: {response}")

    return response


def fetch_places_data(key, place_id, type):
    if 1:
        print(f"Calling Yelp API...")
        client = boto3.client('lambda')

        input_params = dict()
        input_params["place_id"] = place_id
        input_params["type"] = type

        response = client.invoke(
            FunctionName="arn:aws:lambda:us-east-1:992229545431:function:yelp_detail_lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps(input_params)
        )
        result = json.load(response['Payload'])
        print(f"result (from Yelp API): {result}")
    else:
        print(f"Calling Google Places API...")
        # defining Places object for all of Google API's Places related queries
        result = places_api.Places(key=key).place_detail(place_id)
        print(f"result from Place Detail API for {place_id}: {result}")

    return result


def lambda_handler(event, context):
    # TODO implement
    print(f"event: {event}")

    params = event.get("queryStringParameters")
    if not params:
        params = dict()

    place_id = params.get("placeId", "szM1B9tHQixNsmTZTfKoWA")
    place_type = params.get("placeType", "bar")
    print(f"place_id: {place_id}")

    username = str(params.get("username", "foo"))
    print(f"username: {username}")

    # getting google API key
    key = GOOGLE_KEY

    # find place details for the place_id
    result = fetch_places_data(key=key, place_id=place_id, type=place_type)
    print(f"result from Place Detail API for {place_id}: {result}")

    # store user click activity and places related data into OpenSearch and DynamoDB
    store_user_activity_and_places_data_into_os_db(username, place_id, result)

    # put_user_search_activity_into_dynamodb(username, place_id)
    # put_places_data_into_dynamodb(copy.copy(result), place_id)
    # index_places_in_opensearch(result)

    # appending place's live forecast data into its details
    name = result["result"]["name"]
    vicinity = result["result"]["vicinity"]
    compound_code = result["result"]["plus_code"]["compound_code"]
    address = ", ".join([vicinity, ", ".join(compound_code.split(",")[1:])])

    try:
        ret = get_live_forecast(name=name, address=address)
        ret = json.loads(ret["body"])

        result["result"]["busyness_status"] = ret["busyness_status"]
        result["result"]["avg_dwell_time"] = ret["avg_dwell_time"]
        result["result"]["max_dwell_time"] = ret["max_dwell_time"]
    except:
        print(f"Live Forecast API failed. Skipping!!")

    # preparing return dict
    ret = dict()
    ret["headers"] = {
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET'
    }
    ret["statusCode"] = 200
    ret["body"] = json.dumps(result)
    return ret
