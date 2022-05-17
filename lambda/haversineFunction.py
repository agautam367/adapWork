import json
from haversine import haversine, Unit


def lambda_handler(event, context):
    # TODO implement

    print(event)
    places = event["places"]
    user_lat = event["latitude"]
    user_long = event["longitude"]
    print(places)

    print(f"User Latitude: {user_lat}")
    print(f"User Longitude: {user_long}")

    user_coordinates = user_lat, user_long

    for item in places:
        curr_lat = item["geometry"]["location"]["lat"]
        curr_long = item["geometry"]["location"]["lng"]
        print(f"Curr Latitude: {curr_lat}")
        print(f"Curr Longitude: {curr_long}")
        curr_coordinates = curr_lat, curr_long
        item["distance"] = haversine(user_coordinates, curr_coordinates, unit=Unit.MILES)

    print("Distance key added: ")
    print(places)

    return places

