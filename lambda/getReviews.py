import json
import requests
import boto3
from boto3.dynamodb.conditions import Key
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection
from dynamodb_json import json_util as ddjson


def lambda_handler(event, context):
    # TODO implement

    params = event.get("queryStringParameters")
    if not params:
        params = dict()

    place_id = str(params.get("place_id", "123"))

    host = "search-reviews-wnwvb7clbbpbaork2l4mubnbim.us-east-1.es.amazonaws.com"
    region = "us-east-1"

    service = 'es'
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
    index_name = "reviews"

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
                'place_id': place_id,
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
    # print("Line 61")

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    # users_table = dynamodb.Table('reviews')
    table = dynamodb.Table('reviews')

    ans = []

    for i in range(0, totalValues):
        print(response['hits']['hits'][i]['_source']['review_id'])
        res = response['hits']['hits'][i]['_source']['review_id']
        item = table.query(KeyConditionExpression=Key('review_id').eq(str(res)))
        print(item['Items'][0])
        ans.append(item['Items'][0])

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