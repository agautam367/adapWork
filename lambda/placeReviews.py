import json
import datetime
import boto3
from dynamodb_json import json_util as ddjson
from requests_aws4auth import AWS4Auth
from opensearchpy import OpenSearch, RequestsHttpConnection


def put_user_search_activity_into_dynamodb(user_id, item):
    session = boto3.Session()
    ddb = session.client("dynamodb")
    table = "user_activity"

    upd_item = dict()
    upd_item["event_date_time"] = {"N": str(item["event_date_time"])}
    upd_item["event_type"] = {"S": "review"}
    upd_item["place_ids"] = {"L": [{"S": str(item["place_id"])}]}
    upd_item["username"] = {"S": str(item["user_id"])}
    upd_item["activity_id"] = {"S": f"{item['user_id']}_{item['event_date_time']}"}

    response = ddb.put_item(TableName=table, Item=upd_item)
    print(f"response from dynamodb after putting user activity: {response}")


def index_places_in_opensearch(place_id, review_id):
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

    document = dict()
    document["place_id"] = place_id
    document["review_id"] = review_id

    ret = search.index(
        index=index_name,
        body=document,
        id=review_id,
        refresh=False
    )
    print(f"response from opensearch.index call: {ret}")


def get_sentiment(comment):
    client = boto3.client('comprehend')
    response = client.detect_sentiment(Text=comment, LanguageCode="en")
    print(f"response from AWS Comprehend: {response}")
    sentiment = response["Sentiment"]
    return sentiment


def get_key_phrases(comment):
    client = boto3.client('comprehend')
    response = client.detect_key_phrases(Text=comment, LanguageCode="en")
    print(f"response from AWS Comprehend: {response}")
    key_phrases = response["KeyPhrases"]
    return key_phrases


def lambda_handler(event, context):
    # TODO implement

    print(f"event: {event}")

    params = event.get("queryStringParameters")
    if not params:
        params = dict()

    curr_dt = int(datetime.datetime.now().strftime("%Y%m%d%H%M%S"))
    user_id = str(params.get("username", "foo"))
    place_id = str(params.get("place_id", "123"))
    rating = int(params.get("rating", 4.0))
    comment = str(params.get("comment", "Good comment!"))
    review_id = f"{user_id}_{place_id}_{curr_dt}"

    print(f"Rating: {rating}")
    print(f"Comment: {comment}")
    print(f"user_id: {user_id}")

    # put reviews and review analysis into boto3
    session = boto3.Session()
    ddb = session.client("dynamodb")
    table = "reviews"

    item = dict()
    item["event_date_time"] = curr_dt
    item["user_id"] = user_id
    item["place_id"] = place_id
    item["rating"] = rating
    item["comment"] = comment
    item["review_id"] = review_id

    if len(comment) > 0:
        # call AWS Comprehend to do sentiment analysis
        sentiment = get_sentiment(comment)
        key_phrases = get_key_phrases(comment)

        print(f"Ouput from AWS Comprehend- sentiment: {sentiment}, key_phrases: {key_phrases}")

        item["sentiment"] = sentiment
        item["key_phrases"] = key_phrases

    upd_item = ddjson.dumps(item)

    print(f"dynamo db jsonified item: {upd_item}")
    response = ddb.put_item(TableName=table, Item=json.loads(upd_item))
    print(f"response from dynamodb: {response}")

    put_user_search_activity_into_dynamodb(user_id, item)
    index_places_in_opensearch(place_id, review_id)

    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
