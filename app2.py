from flask import Flask, render_template, request, session, redirect, url_for
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
from pymongo import MongoClient
from parse_llm import parse_itinerary, parse_optimized_route, parse_question_answer
from query_db import fetch_country_info, calculate_distance
from query_db_hotel import find_best_accommodation
from uuid import uuid4

load_dotenv()

genai.configure(api_key=os.getenv('GEMINI_KEY'))

app = Flask(__name__)
chat_sessions = {}

# MongoDB setup
mongo_client = MongoClient(os.getenv('MONGO_URI'))
db = mongo_client["chat_app"]
shared_chats_collection = db["shared_chats"]

app.secret_key = "super secrettttttttttttttttttttttttttttttttttt"

def get_city_names(itinerary_json):
    # Function to return a list of city names from the itinerary.
    itinerary = itinerary_json.get("itinerary", {})
    cities = itinerary.get("cities", [])
    
    city_names = [city.get("city", "Unknown City") for city in cities]
    print("*" * 50)
    print("cities in itinerary")
    return city_names

def get_hotel_coordinates(itinerary_json):
    # Function to return a list of hotels and their coordinates (latitude, longitude).
    itinerary = itinerary_json.get("itinerary", {})
    cities = itinerary.get("cities", [])

    hotel_info = [
        {
            "hotel_name": city.get("hotel", {}).get("name", "Unknown Hotel"),
            "coordinates": (
                city.get("hotel", {}).get("coordinates", {}).get("latitude", "Unknown Latitude"),
                city.get("hotel", {}).get("coordinates", {}).get("longitude", "Unknown Longitude")
            )
        }
        for city in cities
    ]
    print("*" * 50)
    print("hotels in itinerary")
    return hotel_info

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_query = request.form.get("query")
        days = request.form.get("days")
        budget = request.form.get("budget")
        trip_type = request.form.get("trip_type")

        with open("test_prompt.txt", "r", encoding="utf-8") as f:
            prompt = f.read()

        preferences = {}
        if days:
            preferences["days"] = days
        if budget:
            preferences["budget"] = budget
        if trip_type:
            preferences["trip_type"] = trip_type

        if preferences:
            preferences_str = f'take these into account user preferences days tell how many days of itinerary is preferred: {json.dumps(preferences)}'
            full_prompt = f"{prompt} {user_query} {preferences_str}"
        else:
            full_prompt = f"{prompt} {user_query} + 'if not given assume everything yourself don't ask questions '"

        session_id = session.get('session_id')
        if session_id and session_id in chat_sessions:
            chat = chat_sessions[session_id]
        else:
            model = genai.GenerativeModel("gemini-2.0-flash-exp")
            chat = model.start_chat()
            session_id = os.urandom(8).hex()
            session['session_id'] = session_id
            chat_sessions[session_id] = chat

        response = chat.send_message(full_prompt, generation_config=genai.GenerationConfig(response_mime_type="application/json"))
        response_json = json.loads(response.text)
        closest_details = None
        details = None
        print("got the itinerary starting custom work here")

        if response_json.get("route"):
            answer = parse_optimized_route(response_json)
        elif response_json.get("itinerary"):
            answer = parse_itinerary(response_json)
            city_names = get_city_names(response_json)
            print(city_names)
            print("*" * 50)
            hotels = get_hotel_coordinates(response_json)
            print(hotels)
            print("*" * 50)

            print("fetching country/city info")

            for city in city_names:
                info = fetch_country_info(osmid=city)
                print(info[0])

            print("*" * 50)

            for hotel in hotels:
                info = find_best_accommodation(lat=hotel['coordinates'][0], lon=hotel['coordinates'][1], hotel_name=hotel['hotel_name'])
                print(hotel['hotel_name'])
                print(info)

        else:
            answer = parse_question_answer(response_json)

        chat_history = [
            message._pb.parts[0].text if hasattr(message._pb, "parts") and len(message._pb.parts) > 0 else "No text found"
            for message in chat.history
        ]

        # Save or update chat history for sharing in MongoDB
        existing_chat = shared_chats_collection.find_one({"_id": session_id})
        if existing_chat:
            shared_chats_collection.update_one(
                {"_id": session_id},
                {"$set": {"chat_history": chat_history}}
            )
        else:
            shared_chats_collection.insert_one({
                "_id": session_id,
                "chat_history": chat_history
            })

        shareable_link = url_for('view_shared_chat', share_id=session_id, _external=True)

        return render_template("index.html", answer=answer, details=details, chat_history=chat_history, shareable_link=shareable_link)

    return render_template("index.html", answer=None, details=None, chat_history=None, shareable_link=None)

@app.route("/shared/<share_id>", methods=["GET"])
def view_shared_chat(share_id):
    shared_chat = shared_chats_collection.find_one({"_id": share_id})
    if not shared_chat:
        return "Chat history not found or expired.", 404

    chat_history = shared_chat.get("chat_history", [])
    return render_template("shared_chat.html", chat_history=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
