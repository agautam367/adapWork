import json
from besttime_api import live_forecast_api

# Manish's BESTTIME KEY
# BESTTIME_KEY = "pri_86b239f2597b49a4898b7684366bd7ea"
BESTTIME_KEY = "pri_42f3eed202cf424fa33a4e106ea061c6"


def lambda_handler(event, context):
    # TODO implement
    print(f"event: {event}")

    # ToDo: params object MUST contain all the below REQUIRED and OPTIONAL params
    params = event.get("queryStringParameters")
    if not params:
        params = dict()
    name = params.get("name", "Panera Bread")
    vicinity = params.get("vicinity", "345 Adams Street, Brooklyn")
    compound_code = params.get("compoundCode", "GIBBERISH, NY, USA")

    # overall address
    address = ", ".join([vicinity, ", ".join(compound_code.split(",")[1:])])

    print(f"final venue_name: {name}")
    print(f"final venue_address: {address}")

    result = live_forecast_api.live_forecast_api(key=BESTTIME_KEY, venue_name=name,
                                                 venue_address=address)
    print(f"live_forecast_api result: {result}")

    live_delta = result["analysis"].get("venue_live_forecasted_delta", 0)
    avg_dwell_minutes = result["venue_info"].get("venue_dwell_time_avg", 0)
    max_dwell_minutes = result["venue_info"].get("venue_dwell_time_max", 0)
    live_status = "as busy as usual"
    if live_delta < 0:
        live_status = "less busy than usual"
    elif live_delta > 0:
        live_status = "more busy than usual"

    result = dict()
    result["busyness_status"] = live_status
    result["avg_dwell_time"] = avg_dwell_minutes
    result["max_dwell_time"] = max_dwell_minutes

    print(f"result: {result}")

    ret = dict()
    ret["statusCode"] = 200
    ret["body"] = json.dumps(result)

    return ret
