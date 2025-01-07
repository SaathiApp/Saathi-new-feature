import json

def parse_optimized_route(route_json):
    route = route_json.get("route", {})
    start_point = route.get("start_point", "Unknown Start Point")
    end_point = route.get("end_point", "Unknown End Point")
    optimized_route = route.get("optimized_route", "No optimized route available.")
    transport_mode = route.get("transport_mode", "Unknown Mode of Transport")
    estimated_time = route.get("estimated_time", "Unknown Travel Time")
    
    alternatives = route.get("alternatives", [])
    alternative_routes = []
    for alt in alternatives:
        alt_route = alt.get("route", "No alternative route")
        alt_mode = alt.get("transport_mode", "Unknown Transport Mode")
        alt_time = alt.get("estimated_time", "Unknown Alternative Travel Time")
        alternative_routes.append(f"Alternative Route: {alt_route} via {alt_mode} (Estimated Time: {alt_time})")

    # Combine the details into a string
    result = f"Optimized Route from {start_point} to {end_point}:\n"
    result += f"Optimized Route: {optimized_route}\n"
    result += f"Transport Mode: {transport_mode}\n"
    result += f"Estimated Travel Time: {estimated_time}\n"

    if alternative_routes:
        result += "\nAlternatives:\n" + "\n".join(alternative_routes)

    return result

# def parse_itinerary(itinerary_json):
#     itinerary = itinerary_json.get("itinerary", {})
#     destination = itinerary.get("destination", "Unknown Destination")
    
#     hotel = itinerary.get("hotel", {})
#     hotel_name = hotel.get("name", "Unknown Hotel")
#     hotel_address = hotel.get("address", "Unknown Address")
#     hotel_coordinates = hotel.get("coordinates", {})
#     hotel_latitude = hotel_coordinates.get("latitude", "Unknown Latitude")
#     hotel_longitude = hotel_coordinates.get("longitude", "Unknown Longitude")
#     hotel_check_in = hotel.get("check_in", "Unknown Check-In Time")
#     hotel_check_out = hotel.get("check_out", "Unknown Check-Out Time")
#     hotel_preferences = hotel.get("preferences", "No preferences provided.")
    
#     result = f"Hotel Information for your stay in {destination}:\n"
#     result += f"Hotel Name: {hotel_name}\n"
#     result += f"Address: {hotel_address}\n"
#     result += f"Coordinates: ({hotel_latitude}, {hotel_longitude})\n"
#     result += f"Check-In Time: {hotel_check_in}\n"
#     result += f"Check-Out Time: {hotel_check_out}\n"
#     result += f"Hotel Preferences: {hotel_preferences}\n"
    
#     days = itinerary.get("days", [])
#     for day in days:
#         day_num = day.get("day", "Unknown Day")
#         result += f"\nDay {day_num} Schedule:\n"
#         for activity in day.get("schedule", []):
#             time = activity.get("time", "Unknown Time")
#             activity_name = activity.get("activity", "Unknown Activity")
#             description = activity.get("description", "No Description")
#             location = activity.get("location", "Unknown Location")
#             location_coordinates = activity.get("coordinates", {})
#             latitude = location_coordinates.get("latitude", "Unknown Latitude")
#             longitude = location_coordinates.get("longitude", "Unknown Longitude")
#             activity_type = activity.get("type", "Unknown Type")
            
#             result += f"- {time}: {activity_name} at {location} ({latitude}, {longitude})\n"
#             result += f"  Type: {activity_type}\n"
#             result += f"  Description: {description}\n"
    
#     return result



# def parse_itinerary(itinerary_json):
#     # print(itinerary_json)
#     itinerary = itinerary_json.get("itinerary", {})
#     destination = itinerary.get("destination", "Unknown Destination")
    
#     hotel = itinerary.get("hotel", {})
#     hotel_name = hotel.get("name", "Unknown Hotel")
#     hotel_address = hotel.get("address", "Unknown Address")
#     hotel_coordinates = hotel.get("coordinates", {})
#     hotel_latitude = hotel_coordinates.get("latitude", "Unknown Latitude")
#     hotel_longitude = hotel_coordinates.get("longitude", "Unknown Longitude")
#     hotel_check_in = hotel.get("check_in", "Unknown Check-In Time")
#     hotel_check_out = hotel.get("check_out", "Unknown Check-Out Time")
#     recommendation_reason = hotel.get("recommendation_reason", "No preferences provided.")
    
#     result = f"Hotel Information for your stay in {destination}:\n"
#     result += f"Hotel Name: {hotel_name}\n"
#     result += f"Address: {hotel_address}\n"
#     result += f"Coordinates: ({hotel_latitude}, {hotel_longitude})\n"
#     result += f"Check-In Time: {hotel_check_in}\n"
#     result += f"Check-Out Time: {hotel_check_out}\n"
#     result += f"Hotel Preferences: {recommendation_reason}\n"
    
#     days = itinerary.get("days", [])
#     for day in days:
#         day_num = day.get("day", "Unknown Day")
#         result += f"\nDay {day_num} Schedule:\n"
#         for activity in day.get("schedule", []):
#             time = activity.get("time", "Unknown Time")
#             activity_name = activity.get("activity", "Unknown Activity")
#             description = activity.get("description", "No Description")
#             location = activity.get("location", "Unknown Location")
#             location_coordinates = activity.get("coordinates", {})
#             latitude = location_coordinates.get("latitude", "Unknown Latitude")
#             longitude = location_coordinates.get("longitude", "Unknown Longitude")
#             activity_type = activity.get("type", "Unknown Type")
#             recommendation_reason = activity.get("recommendation_reason", "No specific reason provided.")
            
#             result += f"- {time}: {activity_name} at {location} ({latitude}, {longitude})\n"
#             result += f"  Type: {activity_type}\n"
#             result += f"  Description: {description}\n"
#             result += f"  Recommended because: {recommendation_reason}\n"
    
#     return result
def parse_itinerary(itinerary_json):
    itinerary = itinerary_json.get("itinerary", {})
    destination = itinerary.get("destination", "Unknown Destination")
    
    result = f"Itinerary for your trip to {destination}:\n"

    # Parse the cities
    cities = itinerary.get("cities", [])
    for city in cities:
        city_name = city.get("city", "Unknown City")
        result += f"\nCity: {city_name}\n"
        
        hotel = city.get("hotel", {})
        hotel_name = hotel.get("name", "Unknown Hotel")
        hotel_address = hotel.get("address", "Unknown Address")
        hotel_coordinates = hotel.get("coordinates", {})
        hotel_latitude = hotel_coordinates.get("latitude", "Unknown Latitude")
        hotel_longitude = hotel_coordinates.get("longitude", "Unknown Longitude")
        hotel_check_in = hotel.get("check_in", "Unknown Check-In Time")
        hotel_check_out = hotel.get("check_out", "Unknown Check-Out Time")
        hotel_recommendation_reason = hotel.get("recommendation_reason", "No preferences provided.")
        
        result += f"Hotel Name: {hotel_name}\n"
        result += f"Address: {hotel_address}\n"
        result += f"Coordinates: ({hotel_latitude}, {hotel_longitude})\n"
        result += f"Check-In Time: {hotel_check_in}\n"
        result += f"Check-Out Time: {hotel_check_out}\n"
        result += f"Hotel Preferences: {hotel_recommendation_reason}\n"
        
        # Parse sub-trip (whole city as one sub-trip)
        sub_trip_num = 1
        result += f"\nSub-Trip {sub_trip_num} - Schedule for {city_name}:\n"
        
        # Get the days for the sub-trip (city)
        sub_trips = city.get("sub_trips", [])
        for sub_trip in sub_trips:
            for day in sub_trip.get("days", []):
                day_num = day.get("day", "Unknown Day")
                result += f"\nDay {day_num}:\n"
                for activity in day.get("schedule", []):
                    time = activity.get("time", "Unknown Time")
                    activity_name = activity.get("activity", "Unknown Activity")
                    description = activity.get("description", "No Description")
                    location = activity.get("location", "Unknown Location")
                    location_coordinates = activity.get("coordinates", {})
                    activity_latitude = location_coordinates.get("latitude", "Unknown Latitude")
                    activity_longitude = location_coordinates.get("longitude", "Unknown Longitude")
                    activity_type = activity.get("type", "Unknown Type")
                    activity_recommendation_reason = activity.get("recommendation_reason", "No specific reason provided.")
                    
                    result += f"- {time}: {activity_name} at {location} ({activity_latitude}, {activity_longitude})\n"
                    result += f"  Type: {activity_type}\n"
                    result += f"  Description: {description}\n"
                    result += f"  Recommended because: {activity_recommendation_reason}\n"
    
    return result


def parse_question_answer(qna_json):
    question = qna_json.get("question", "Unknown Question")
    answer = qna_json.get("answer", "No answer available.")
    sources = qna_json.get("sources", "No sources provided.")
    
    result = f"Question: {question}\n"
    result += f"Answer: {answer}\n"
    result += f"Sources: {sources}\n"
    
    return result

# Sample Data (replace with actual JSON data)

# Parse and display results
# print(parse_optimized_route(route_json))
# print("\n" + "-"*40 + "\n")
# print(parse_itinerary(itinerary_json))
# print("\n" + "-"*40 + "\n")
# print(parse_question_answer(qna_json))
