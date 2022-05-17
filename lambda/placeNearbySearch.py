import json
import boto3
from google_api import places_api
from google_api import geocode_api
from google_api import geolocate_api
import datetime
from dynamodb_json import json_util as ddjson
from boto3.dynamodb.conditions import Key
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
import copy

# import haversine


# Google API Personal Key (Manish)
GOOGLE_KEY = "AIzaSyDAEnmrfeFCXgLgOa_gWKfq5XKrOYs_GBs"


def store_user_activity_and_places_data_into_os_db(user_name, top_n_places):
    client = boto3.client('lambda')

    input_params = dict()
    input_params["user_name"] = user_name
    input_params["top_n_places"] = top_n_places

    client.invoke(
        FunctionName="arn:aws:lambda:us-east-1:992229545431:function:storePlacesNearbySearch",
        InvocationType='Event',
        Payload=json.dumps(input_params)
    )
    # response = json.load(response['Payload'])
    # return response


def get_live_forecast(name, address):
    client = boto3.client('lambda')

    input_params = dict()
    input_params["venue_name"] = name
    input_params["venue_address"] = address

    response = client.invoke(
        FunctionName="arn:aws:lambda:us-east-1:992229545431:function:placeLiveForecast",
        InvocationType='RequestResponse',
        Payload=json.dumps(input_params)
    )
    response = json.load(response['Payload'])
    return response


def haversineFunction(places, curr_lat, curr_long):
    client = boto3.client('lambda')

    input_params = dict()
    input_params["places"] = places
    input_params["latitude"] = curr_lat
    input_params["longitude"] = curr_long

    response = client.invoke(
        FunctionName="arn:aws:lambda:us-east-1:992229545431:function:haversineFunction",
        InvocationType='RequestResponse',
        Payload=json.dumps(input_params)
    )
    response = json.load(response['Payload'])
    return response


# def recommendFunction(curr_lat, curr_long):
#     client = boto3.client('lambda')

#     input_params = dict()
#     input_params["latitude"] = curr_lat
#     input_params["longitude"] = curr_long

#     response = client.invoke(
#         FunctionName = "arn:aws:lambda:us-east-1:992229545431:function:recommendFunction",
#         InvocationType = 'RequestResponse',
#         Payload = json.dumps(input_params)
#     )
#     response = json.load(response['Payload'])
#     return response


def clean_params(params):
    upd_params = dict()
    for param, value in params.items():
        if value is not None and value.lower() != "none" and value.lower() != "undefined" and value != "null":
            upd_params[param] = value
    return upd_params


# def put_image_into_s3(iname, oname):
#     s3 = boto3.client("s3")
#     with open(iname, 'rb') as file_obj:
#         s3_upload = s3.put_object( Bucket="adapwork-places-images", Key=f"{oname}.png", Body=file_obj)


# def put_user_search_activity_into_dynamodb(user_id, places_data):
#     session = boto3.Session()
#     ddb = session.client("dynamodb")
#     table = "user_activity"

#     curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     item = dict()
#     item["event_date_time"] = {"N": curr_dt}
#     item["event_type"] = {"S": "search"}
#     item["place_ids"] = {"L": [{"S": place_data["place_id"]} for place_data in places_data]}
#     item["username"] = {"S": user_id}
#     item["activity_id"] = {"S": f"{user_id}_{curr_dt}"}

#     response = ddb.put_item(TableName=table, Item=item)
#     print(f"response from dynamodb after putting user activity: {response}")


# def put_places_data_into_dynamodb(places_data):
#     session = boto3.Session()
#     ddb = session.client("dynamodb")
#     table = "places"
#     ddob = boto3.resource('dynamodb', region_name='us-east-1')
#     tableobj = ddob.Table(table)

#     # curr_dt = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     # item = dict()
#     # item["event_date_time"] = {"N": curr_dt}
#     # item["event_type"] = {"S": "search"}
#     # item["place_ids"] = {"L": [{"S": place_data["place_id"]} for place_data in places_data]}
#     # item["username"] = {"S": user_id}
#     # item["activity_id"] = {"S": f"{user_id}_{curr_dt}"}

#     for item in places_data:
#         place_id = item["place_id"]

#         # check if the place is already present
#         check_item = tableobj.query(KeyConditionExpression=Key('place_id').eq(str(place_id)))

#         if len(check_item["Items"]) > 0:
#             print(f"place_id: {place_id} ALREADY found in DynamoDB: {check_item['Items']}")
#             upd_item = check_item["Items"][0]
#             upd_item["search_count"] += 1
#             upd_item = ddjson.dumps(upd_item)
#         else:
#             print(f"place_id: {place_id} NOT found in DynamoDB: {check_item['Items']}")
#             open_status = item.get("opening_hours", {}).get("open_now", None)
#             if open_status is not None:
#                 if str(open_status).lower() == "true":
#                     open_status = True
#                 elif str(open_status).lower() == "false":
#                     open_status = False
#                 item["opening_hours"]["open_now"] = open_status
#             item["search_count"] = 1
#             item["interested_count"] = item["clicked_count"] = 0
#             upd_item = ddjson.dumps(item)

#         # print(f"dynamo db jsonified item: {upd_item}")
#         response = ddb.put_item(TableName=table, Item=json.loads(upd_item))
#         # print(f"response from dynamodb: {response}")
#         print("response from dynamodb")
#         # break


# def index_places_in_opensearch(places_data):
#     host = "search-places-wx453xoejioxp76jewe3ae6xlm.us-east-1.es.amazonaws.com"
#     region = "us-east-1"

#     service = 'es'
#     credentials = boto3.Session().get_credentials()
#     awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
#     index_name = "places"

#     search = OpenSearch(
#         hosts=[{'host': host, 'port': 443}],
#         http_auth=awsauth,
#         use_ssl=True,
#         verify_certs=True,
#         connection_class=RequestsHttpConnection
#     )

#     for place_data in places_data:
#         place_id = place_data["place_id"]

#         document = dict()
#         document["place_id"] = place_data["place_id"]
#         document["place_types"] = place_data["types"]
#         document["postal_code"] = place_data["plus_code"]["compound_code"][:4]
#         # print(f"document (to be inserted) in OpenSearch: {document}")

#         # flag = 0
#         # for item in place_data["result"]["address_components"]:
#         #     types = item["types"]
#         #     for typ in types:
#         #         if typ == "postal_code":
#         #             document["postal_code"] = item["long_name"]
#         #             flag=1
#         #             break
#         #     if flag == 1:
#         #         break
#         # # documents["place_id"] = place_data["place_id"]

#         ret = search.index(
#                     index = index_name,
#                     body = document,
#                     id = place_id,
#                     refresh = True
#                 )
#         # print(f"response from opensearch.index call: {ret}")


# def add_distance(places, user_lat, user_long):
#     print(f"User Latitude: {user_lat}")
#     print(f"User Longitude: {user_long}")

#     user_coordinates = user_lat, user_long

#     for item in places:
#         curr_lat = item["geometry"]["location"]["lat"]
#         curr_long = item["geometry"]["location"]["lng"]
#         print(f"Curr Latitude: {curr_lat}")
#         print(f"Curr Longitude: {curr_long}")
#         curr_coordinates = curr_lat, curr_long
#         item["distance"] = haversine(user_coordinates, curr_coordinates, unit=Unit.MILES)

#     print("Distance key added: ")
#     print(places)

#     return places


def fetch_places_data(key, type, location, radius, minprice, maxprice, opennow, rankby):
    if 1:
        print(f"Calling Yelp API...")
        client = boto3.client('lambda')

        input_params = dict()
        input_params["type"] = type
        input_params["location"] = location
        input_params["radius"] = radius
        input_params["minprice"] = minprice
        input_params["maxprice"] = maxprice
        input_params["opennow"] = opennow
        input_params["rankby"] = rankby

        response = client.invoke(
            FunctionName="arn:aws:lambda:us-east-1:992229545431:function:yelp_lambda",
            InvocationType='RequestResponse',
            Payload=json.dumps(input_params)
        )
        result = json.load(response['Payload'])
        print(f"result (from Yelp API): {result}")
    else:
        print(f"Calling Google Places API...")
        # defining Places object for all of Google API's Places related queries
        pobj = places_api.Places(key=key, type=place_type, location=geocodes, radius=radius, minprice=minprice,
                                 maxprice=maxprice, opennow=opennow, rankby=rankby)
        # find places near desired geo codes
        result = pobj.places_nearby_search()
        print(f"result (from Google API): {result}")

    return result


def lambda_handler(event, context):
    # TODO implement
    print(f"event: {event}")

    # ToDo: event object MUST contain all the below REQUIRED and OPTIONAL params
    params = event.get("queryStringParameters")
    if not params:
        params = dict()
    params = clean_params(params)

    n = int(params.get("numResults", 20))  # how many search results to return
    # ToDo: support multiple places types at once here
    place_type = params.get("placeType", "bar")  # Check google_places_api.py for all supported types
    radius = int(params.get("radius", 1000))  # in meters
    minprice = int(params.get("minPrice", 0))
    maxprice = int(params.get("maxPrice", 4))
    opennow = bool(params.get("openNow", False))
    rankby = params.get("rankBy", "prominence")  # values can be [prominence, distance]
    text_location = params.get("textLocation", "5 MetroTech Center, Jay Street, Brooklyn")
    tmp = params.get("useCurrentLocation")
    if tmp is None:
        use_given_loc = False
    else:
        if str(tmp).lower() == "true":
            use_given_loc = False
        else:
            use_given_loc = True
    # use_given_loc = bool(not params.get("useCurrentLocation", False))  # whether to use the "given text" location or the "current" location for nearby search
    curr_lat = float(params.get("currentLat", 0))
    curr_long = float(params.get("currentLong", 0))
    username = str(params.get("username", "foo"))
    print("TEXT LOCATION: ")
    print(text_location)
    # getting google API key
    key = GOOGLE_KEY

    # get geocodes nearby which we want to find places
    geocodes = None
    if use_given_loc:
        # get geocode for "given text" location
        result = geocode_api.Geocode(key=key).geocoding_the_googleplex(location=text_location)
        _loc = result[0]["geometry"]["location"]
        given_geocodes = _loc["lat"], _loc["lng"]
        geocodes = given_geocodes
        print("TEXT SEARCH GEOCODES: ")
        print(geocodes)
    else:
        # get geocode for "current" location
        # gl = geolocate_api.GeoLocation(key=key).geolocate()
        # curr_geocodes, accuracy = (gl["location"]["lat"], gl["location"]["lng"]), gl["accuracy"]
        # geocodes = curr_geocodes
        geocodes = curr_lat, curr_long
        print("CURR LOCATION GEOCODES: ")
        print(geocodes)
    print(f"geocodes: {geocodes}")

    # make API call to fetch places data
    result = fetch_places_data(key=key, type=place_type, location=geocodes, radius=radius, minprice=minprice,
                               maxprice=maxprice, opennow=opennow, rankby=rankby)

    # # defining Places object for all of Google API's Places related queries
    # pobj = places_api.Places(key=key, type=place_type, location=geocodes, radius=radius, minprice=minprice,
    #                           maxprice=maxprice, opennow=opennow, rankby=rankby)

    # # find places near desired geo codes
    # result = pobj.places_nearby_search()

    places = result["results"]
    print(f"len(results) from google places api: {len(places)}")

    # extracting top 10 results
    top_n_places = places[:n]

    # # put user search activity into "user_activity" dynamo db
    # put_user_search_activity_into_dynamodb(username, top_n_places)

    # # put places (nearby search) data into dynamo db
    # put_places_data_into_dynamodb(top_n_places)

    # # index places data in opensearch
    # index_places_in_opensearch(top_n_places)

    # store places nearby search related data into OpenSearch and DynamoDB
    store_user_activity_and_places_data_into_os_db(username, top_n_places)

    # add distance in top_n_places
    final_res = haversineFunction(places=top_n_places, curr_lat=curr_lat, curr_long=curr_long)

    print("Final Result after distance: ")
    print(final_res)

    # # get images for top n places
    # for i in range(len(top_n_places)):
    #     photo_data = top_n_places[i]["photos"][0]
    #     ref = photo_data["photo_reference"]
    #     width = photo_data["width"]
    #     height = photo_data["height"]
    #     img = pobj.photo(ref=ref, width=width, height=height)
    #     print(f"img fetched from Photos API: {type(img)}")

    #     # creating temporary image file locally
    #     print(f"reading image into a file: start")
    #     tmpf = "/tmp/tmp12.jpg"
    #     with open(tmpf, "wb") as f:
    #         for chunk in img:
    #             if chunk:
    #                 f.write(chunk)
    #     print(f"reading image into a file: end")

    #     print(f"putting image onto the s3 bucket...")
    #     put_image_into_s3(iname=tmpf, oname=ref)

    # get live occupancy status and average dwell time for the top n places
    # for i in range(len(top_n_places)):
    #     name = top_n_places[i]["name"]
    #     vicinity = top_n_places[i]["vicinity"]
    #     compound_code = top_n_places[i]["plus_code"]["compound_code"]
    #     address = ", ".join([vicinity, ", ".join(compound_code.split(",")[1:])])

    #     result = get_live_forecast(name=name, address=address)

    #     top_n_places[i]["busyness_status"] = result["busyness_status"]
    #     top_n_places[i]["avg_dwell_time"] = result["avg_dwell_time"]
    #     top_n_places[i]["max_dwell_time"] = result["max_dwell_time"]

    # print(f"top {n} places: {top_n_places}")

    ret = dict()
    ret["headers"] = {
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET'
    }
    ret["statusCode"] = 200
    ret["body"] = json.dumps(final_res)

    return ret
