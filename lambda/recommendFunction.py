import json
import requests
import boto3
from boto3.dynamodb.conditions import Key
from requests_aws4auth import AWS4Auth
from dynamodb_json import json_util as ddjson
from opensearchpy import OpenSearch, RequestsHttpConnection
import geopy


def find_open_search(zip_code):
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

    # Search for the document.
    # q = 'indian'
    query = {
        'query': {
            'match': {
                'postal_code': zip_code,
            }
        }
    }

    response = search.search(
        body=query,
        index=index_name
    )
    print(f'Response from OpenSearch: {response}')

    totalValues = response['hits']['total']['value']
    print(totalValues)

    if totalValues > 20:
        totalValues = 20
    print(totalValues)

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # users_table = dynamodb.Table('reviews')
    table = dynamodb.Table('places')

    ans = []

    for i in range(0, totalValues):
        print(response['hits']['hits'][i]['_source']['place_id'])
        res = response['hits']['hits'][i]['_source']['place_id']
        item = table.query(KeyConditionExpression=Key('place_id').eq(str(res)))
        print(item['Items'][0])
        ans.append(item['Items'][0])

    return ans


def lambda_handler(event, context):
    # TODO implement

    params = event.get("queryStringParameters")
    if not params:
        params = dict()

    curr_lat = float(params.get("currentLat", 40.7128))
    curr_long = float(params.get("currentLong", -74.0060))

    geo_locator = geopy.Nominatim(user_agent='1234')
    location = (curr_lat, curr_long)

    r = geo_locator.reverse(location)
    print(r.raw)
    zip_code = r.raw['address']['postcode']
    print(zip_code)
    zip_code = 1120

    ans = find_open_search(zip_code)

    ans = ddjson.loads(ans)
    print("ANSWER")
    print(ans)
    print(len(ans))
    # return ans
    ret = dict()
    ret["headers"] = {
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET'
    }
    ret["statusCode"] = 200
    ret["body"] = json.dumps(ans)

    return ret
