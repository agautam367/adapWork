import json
import boto3
import datetime
from dynamodb_json import json_util as ddjson
from boto3.dynamodb.conditions import Key
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
import copy


def put_user_search_activity_into_dynamodb(user_id, places_data):
    session = boto3.Session()
    ddb = session.client("dynamodb")
    table = "user_activity"

    curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    item = dict()
    item["event_date_time"] = {"N": curr_dt}
    item["event_type"] = {"S": "search"}
    item["place_ids"] = {"L": [{"S": place_data["place_id"]} for place_data in places_data]}
    item["username"] = {"S": user_id}
    item["activity_id"] = {"S": f"{user_id}_{curr_dt}"}

    response = ddb.put_item(TableName=table, Item=item)
    print(f"response from dynamodb after putting user activity: {response}")


def put_places_data_into_dynamodb(places_data):
    session = boto3.Session()
    ddb = session.client("dynamodb")
    table = "places"
    ddob = boto3.resource('dynamodb', region_name='us-east-1')
    tableobj = ddob.Table(table)

    # curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    # item = dict()
    # item["event_date_time"] = {"N": curr_dt}
    # item["event_type"] = {"S": "search"}
    # item["place_ids"] = {"L": [{"S": place_data["place_id"]} for place_data in places_data]}
    # item["username"] = {"S": user_id}
    # item["activity_id"] = {"S": f"{user_id}_{curr_dt}"}

    for item in places_data:
        place_id = item["place_id"]

        # check if the place is already present
        check_item = tableobj.query(KeyConditionExpression=Key('place_id').eq(str(place_id)))

        if len(check_item["Items"]) > 0:
            print(f"place_id: {place_id} ALREADY found in DynamoDB: {check_item['Items']}")
            upd_item = check_item["Items"][0]
            upd_item["search_count"] += 1
            upd_item = ddjson.dumps(upd_item)
        else:
            print(f"place_id: {place_id} NOT found in DynamoDB: {check_item['Items']}")
            open_status = item.get("opening_hours", {}).get("open_now", None)
            if open_status is not None:
                if str(open_status).lower() == "true":
                    open_status = True
                elif str(open_status).lower() == "false":
                    open_status = False
                item["opening_hours"]["open_now"] = open_status
            item["search_count"] = 1
            item["interested_count"] = item["clicked_count"] = 0
            upd_item = ddjson.dumps(item)

        # print(f"dynamo db jsonified item: {upd_item}")
        response = ddb.put_item(TableName=table, Item=json.loads(upd_item))
        # print(f"response from dynamodb: {response}")
        print("response from dynamodb")
        # break


def index_places_in_opensearch(places_data):
    host = "search-places-wx453xoejioxp76jewe3ae6xlm.us-east-1.es.amazonaws.com"
    region = "us-east-1"

    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    index_name = "places"

    search = OpenSearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    for place_data in places_data:
        place_id = place_data["place_id"]

        document = dict()
        document["place_id"] = place_data["place_id"]
        document["place_types"] = place_data["types"]
        document["postal_code"] = place_data["plus_code"]["compound_code"]
        # print(f"document (to be inserted) in OpenSearch: {document}")

        # flag = 0
        # for item in place_data["result"]["address_components"]:
        #     types = item["types"]
        #     for typ in types:
        #         if typ == "postal_code":
        #             document["postal_code"] = item["long_name"]
        #             flag=1
        #             break
        #     if flag == 1:
        #         break
        # # documents["place_id"] = place_data["place_id"]

        ret = search.index(
            index=index_name,
            body=document,
            id=place_id,
            refresh=True
        )
        print(f"response from opensearch.index call: {ret}")


def lambda_handler(event, context):
    # TODO implement
    print(f"event: {event}")

    username = event["user_name"]
    top_n_places = event["top_n_places"]

    # put user search activity into "user_activity" dynamo db
    put_user_search_activity_into_dynamodb(username, top_n_places)

    # put places (nearby search) data into dynamo db
    put_places_data_into_dynamodb(top_n_places)

    # index places data in opensearch
    index_places_in_opensearch(top_n_places)

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
