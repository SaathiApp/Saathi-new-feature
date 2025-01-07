from flask import Flask, render_template, request,session
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
from parse_llm import parse_itinerary, parse_optimized_route, parse_question_answer
from query_db import fetch_country_info, calculate_distance
from query_db_hotel import find_best_accommodation
load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_KEY'))

app = Flask(__name__)
chat_sessions = {}
app.secret_key = "super secrettttttttttttttttttttttttttttttttttt"
def get_city_names(itinerary_json):
    """
    Function to return a list of city names from the itinerary.
    """
    itinerary = itinerary_json.get("itinerary", {})
    cities = itinerary.get("cities", [])
    
    city_names = []
    for city in cities:
        city_name = city.get("city", "Unknown City")
        city_names.append(city_name)
    print("*"*50)
    print("cities in itenary")
    return city_names

def get_hotel_coordinates(itinerary_json):
    """
    Function to return a list of hotels and their coordinates (latitude, longitude).
    """
    itinerary = itinerary_json.get("itinerary", {})
    cities = itinerary.get("cities", [])
    
    hotel_info = []
    for city in cities:
        hotel = city.get("hotel", {})
        hotel_name = hotel.get("name", "Unknown Hotel")
        hotel_coordinates = hotel.get("coordinates", {})
        hotel_latitude = hotel_coordinates.get("latitude", "Unknown Latitude")
        hotel_longitude = hotel_coordinates.get("longitude", "Unknown Longitude")
        
        hotel_info.append({
            "hotel_name": hotel_name,
            "coordinates": (hotel_latitude, hotel_longitude)
        })
    print("*"*50)
    print("hotels in itenary")
    return hotel_info






@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":
        
        user_query = request.form.get("query")
        days = request.form.get("days")
        budget = request.form.get("budget")
        trip_type = request.form.get("trip_type")
        
        with open("prompt.txt", "r", encoding="utf-8") as f:
            prompt = f.read()
        
        preferences = {}
        if days:
            preferences["days"] = days
        if budget:
            preferences["budget"] = budget
        if trip_type:
            preferences["trip_type"] = trip_type
        
        if preferences:
            preferences_str = f'take these into account user preferences days tell how many days of itenary is preffered: {json.dumps(preferences)}'
            full_prompt = f"{prompt} {user_query} {preferences_str}"
        else:
            full_prompt = f"{prompt} {user_query}+'if not given assume everything yourself dont ask questions '"
            # full_prompt = f"{prompt} {user_query}"

        session_id = session.get('session_id')
        if session_id and session_id in chat_sessions:
            chat = chat_sessions[session_id]  
        else:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            chat = model.start_chat()  
            session_id = os.urandom(8).hex()  
            session['session_id'] = session_id
            chat_sessions[session_id] = chat
        # print(chat.history)
        # response = model.generate_content(full_prompt, generation_config=genai.GenerationConfig(response_mime_type="application/json"))
        response = chat.send_message(full_prompt, generation_config=genai.GenerationConfig(response_mime_type="application/json"))
        response_json = json.loads(response.text)
        # print(response_json)
        closest_details = None
        details = None
        print("got the itenary starting custom work here")
        if response_json.get("route"):
            answer = parse_optimized_route(response_json)
        elif response_json.get("itinerary"):
            
            answer = parse_itinerary(response_json)
            city_names = get_city_names(response_json)
            print(city_names)
            print("*"*50)
            hotels = get_hotel_coordinates(response_json)
            print(hotels)
            print("*"*50)

            print("fetching country/city info")
            
            for city in city_names:
                info = fetch_country_info(osmid=city)
                print(info[0])

            print("*"*50)

            for hotel in hotels:
                # print(hotel)  
                info = find_best_accommodation(lat=hotel['coordinates'][0], lon=hotel['coordinates'][1], hotel_name=hotel['hotel_name'])
                print(hotel['hotel_name'])
                print(info)

        else:
            answer = parse_question_answer(response_json)



        chat_history = []
        # print(chat.history[0].__dict__)
        # print(chat.history[0]['parts'])
        for message in chat.history:
      
            pb_obj = message._pb

       
            if hasattr(pb_obj, "parts") and len(pb_obj.parts) > 0:
                chat_history.append(pb_obj.parts[0].text)
            else:
                chat_history.append("No text found")
        return render_template("index.html", answer=answer, details=details,chat_history=chat_history)

    return render_template("index.html", answer=None, details=None,chat_history=None)

if __name__ == "__main__":
    app.run(debug=True)
