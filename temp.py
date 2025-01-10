# import requests
# import json

# def get_hotel_by_name(hotel_name, output_filename):
#     """
#     Fetch hotel details by name using the Overpass API.

#     Args:
#         hotel_name (str): Name of the hotel to search for.
#         output_filename (str): File name to save the hotel data as JSON.

#     Returns:
#         dict: A dictionary containing hotel details if found, else None.
#     """

#     OVERPASS_URL = "https://overpass-api.de/api/interpreter"
    
#     # Query to search for hotels with the specific name
#     query = f"""
#     [out:json];
#     (
#       node["tourism"="hotel"]["name"="{hotel_name}"];
#       way["tourism"="hotel"]["name"="{hotel_name}"];
#       relation["tourism"="hotel"]["name"="{hotel_name}"];
#     );
#     out body;
#     """

#     try:
#         # Sending the request to Overpass API
#         response = requests.post(OVERPASS_URL, data={"data": query})
#         response.raise_for_status()

#         # Parse the JSON response
#         data = response.json()
        
#         # Check if any results were returned
#         if not data.get("elements"):
#             print(f"No hotel found with the name: {hotel_name}")
#             return None
        
#         # Process the first hotel found (you can adjust to handle multiple results)
#         hotel = data["elements"][0]
        
#         # Extract relevant information
#         tags = hotel.get("tags", {})
#         center = hotel.get("center", {})
#         uid = hotel.get('id', "")
        
#         hotel_details = {
#             "name": tags.get("name", "Unnamed Hotel"),
#             "latitude": center.get("lat", "Unknown"),
#             "longitude": center.get("lon", "Unknown"),
#             "id": uid,
#             "tags": tags
#         }
        
#         # Save the result to a JSON file
#         with open(output_filename, "w", encoding="utf-8") as f:
#             json.dump(hotel_details, f, ensure_ascii=False, indent=4)

#         print(f"Hotel data saved to {output_filename}")
#         return hotel_details

#     except requests.exceptions.RequestException as e:
#         print(f"An error occurred while querying the Overpass API: {e}")
#         return None
#     except json.JSONDecodeError as e:
#         print(f"Error decoding JSON response: {e}")
#         return None
# hotel_name = "Conch Building"
# output_filename = "hotel_data.json"

# hotel_info = get_hotel_by_name(hotel_name, output_filename)

# if hotel_info:
#     print("Hotel found:", hotel_info)
# else:
#     print("Hotel not found.")
from dataclasses import dataclass
from typing import List
from enum import Enum

class Role(str, Enum):
    USER = "user"
    MODEL = "model"

@dataclass
class Part:
    text: str

    def __str__(self):
        return f'parts {{ text: "{self.text}" }}'

@dataclass
class ChatMessage:
    parts: List[Part]
    role: Role

    def __str__(self):
        parts_str = ", ".join(str(part) for part in self.parts)
        return f'{parts_str}\nrole: "{self.role}"'
    
    def __repr__(self):
        # This is what we're returning when the object is printed in a list
        return self.__str__()

class ChatHistory(list):
    def append(self, message: ChatMessage) -> None:
        if not isinstance(message, ChatMessage):
            raise TypeError("Can only append ChatMessage objects")
        super().append(message)
    
    def __str__(self):
        return "[\n" + ",\n".join(str(msg) for msg in self) + "\n]"

def create_user_message(text: str) -> ChatMessage:
    return ChatMessage(parts=[Part(text=text)], role="user")

def create_model_message(text: str) -> ChatMessage:
    return ChatMessage(parts=[Part(text=text)], role="model")








from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_KEY'))
model = genai.GenerativeModel("gemini-1.5-flash")

chat = model.start_chat(
            history=[
                {"role": "user", "parts": "My name is namit"},
                {"role": "model", "parts": "Hi nice to meet you"},
            ]
        )


# res = chat.send_message("what is my name")


# print(chat.history)

















