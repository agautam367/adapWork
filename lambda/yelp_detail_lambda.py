import json
import requests


def yelp_output_to_google_output_details(data, type):
    data["place_id"] = data["id"]
    data["opening_hours"] = {}
    if str(data["is_closed"]).lower() == "false":
        data["opening_hours"]["open_now"] = False
    else:
        data["opening_hours"]["open_now"] = True
    data["plus_code"] = {}
    data["plus_code"]["compound_code"] = data["location"]["zip_code"]
    data["types"] = [item["title"] for item in data["categories"]]
    data["types"].append(type)

    data["vicinity"] = data["location"]["address1"]
    data["plus_code"] = {}
    data["plus_code"]["compound_code"] = data["location"]["display_address"][-1]
    data["formatted_address"] = ", ".join(data["location"]["display_address"])

    return data


def yelp_place_details(place_id, type):
    api_key = 'sXPUTTkDDD_gkK0xPOpVCG6m7TZLRY0Zuw_RLXqppfOR5ftQHivUwQyPrR1aVdJWBfJNpyK-0uT7NwN0_SbozZw5f5aA139Tl5_Ig9SWqX0QlTh0wB008z-J19YeYnYx'
    url = 'https://api.yelp.com/v3/businesses/' + place_id

    headers = {'Authorization': 'Bearer {}'.format(api_key)}

    # params = google_input_to_yelp_input(type, location, radius, minprice, maxprice, opennow, rankby)

    response = requests.get(url, headers=headers)
    data_dict = response.json()
    print("DATA_DICT")
    print(data_dict)

    result = yelp_output_to_google_output_details(data_dict, type)
    ret = {}
    ret["result"] = result
    return ret


def lambda_handler(event, context):
    # TODO implement
    print("Event YELP")
    print(event)

    result = yelp_place_details(event["place_id"], event["type"])

    return result

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
