import json
import requests

google_types_to_yelp_types = dict()

google_types_to_yelp_types["bakery"] = "bakery"
google_types_to_yelp_types["bar"] = "bars"
google_types_to_yelp_types["book_store"] = "bookstores"
google_types_to_yelp_types["cafe"] = "cafe"
google_types_to_yelp_types["library"] = "library"
google_types_to_yelp_types["park"] = "park"
google_types_to_yelp_types["restaurant"] = "restaurant"
google_types_to_yelp_types["university"] = "university"


def google_input_to_yelp_input(type, location, radius, minprice, maxprice, opennow, rankby):
    lat = location[0]
    lng = location[1]

    price_level = []

    for i in range(minprice + 1, maxprice + 1):
        price_level.append(str(i))

    price_levels = ",".join(price_level)
    print(price_levels)

    params = {'term': type,
              'latitude': lat,
              'longitude': lng,
              'radius': radius,
              'price': price_levels,
              'open_now': opennow,
              'limit': 20}

    return params


def yelp_output_to_google_output(data, type):
    new_data = []
    for business in data:
        business["place_id"] = business["id"]
        business["opening_hours"] = {}
        if str(business["is_closed"]).lower() == "false":
            business["opening_hours"]["open_now"] = False
        else:
            business["opening_hours"]["open_now"] = True
        business["plus_code"] = {}
        business["plus_code"]["compound_code"] = business["location"]["zip_code"]
        business["types"] = [item["title"] for item in business["categories"]]
        business["types"].append(type)
        business["geometry"] = {}
        business["geometry"]["location"] = {
            "lat": business["coordinates"]["latitude"],
            "lng": business["coordinates"]["longitude"]
        }
        business["formatted_address"] = ", ".join(business["location"]["display_address"])
        new_data.append(business)

    return new_data


def yelp_place_nearby_search(type, location, radius, minprice, maxprice, opennow, rankby):
    api_key = 'sXPUTTkDDD_gkK0xPOpVCG6m7TZLRY0Zuw_RLXqppfOR5ftQHivUwQyPrR1aVdJWBfJNpyK-0uT7NwN0_SbozZw5f5aA139Tl5_Ig9SWqX0QlTh0wB008z-J19YeYnYx'
    url = 'https://api.yelp.com/v3/businesses/search'

    headers = {'Authorization': 'Bearer {}'.format(api_key)}

    params = google_input_to_yelp_input(type, location, radius, minprice, maxprice, opennow, rankby)

    response = requests.get(url, headers=headers, params=params)
    data_dict = response.json()
    print(data_dict["businesses"])

    result = yelp_output_to_google_output(data_dict["businesses"], type)
    ret = {}
    ret["results"] = result
    return ret


def lambda_handler(event, context):
    # TODO implement
    print(event)
    result = yelp_place_nearby_search(event["type"], event["location"], event["radius"], event["minprice"],
                                      event["maxprice"], event["opennow"], event["rankby"])

    return result

    # return {
    #     'statusCode': 200,
    #     'body': json.dumps('Hello from Lambda!')
    # }
