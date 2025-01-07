import mysql.connector
from dotenv import load_dotenv
import os
import string

load_dotenv()

stopwords = {"the", "a", "an", "hotel", "resort", "place", "in", "of", "and", "on", "with", "at"}

def preprocess_text(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    words = text.split()
    words = [word for word in words if word not in stopwords]
    return words

def jaccard_similarity(str1, str2):
    words1 = preprocess_text(str1)
    words2 = preprocess_text(str2)
    set1 = set(words1)
    set2 = set(words2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)
    similarity = len(intersection) / len(union)
    return similarity

def connect_to_db():
    return mysql.connector.connect(
        host=os.getenv('host'),
        user=os.getenv('user'),
        password=os.getenv('password'),
        database=os.getenv('database')
    )

def find_best_accommodation(lat, lon, hotel_name, max_distance_km=5, table_name="accommodations_details"):
    db_connection = connect_to_db()
    cursor = db_connection.cursor()
    lat_rad = float(lat) * (3.141592653589793 / 180)
    lon_rad = float(lon) * (3.141592653589793 / 180)

    query = f"""
    SELECT DISTINCT id, name, latitude, longitude, stars, price_range, website, contact_phone, amenities,
           (6371 * acos(cos({lat_rad}) * cos(radians(latitude)) * cos(radians(longitude) - {lon_rad}) + sin({lat_rad}) * sin(radians(latitude)))) AS distance
    FROM {table_name}
    HAVING distance <= {max_distance_km}
    ORDER BY distance;
    """
    cursor.execute(query)
    
    accommodations = cursor.fetchall()
    # print(accommodations)
    if accommodations:
        selected_hotel = None
        for accommodation in accommodations:
            id, name, latitude, longitude, stars, price_range, website, contact_phone, amenities, distance = accommodation
            similarity_score = jaccard_similarity(str1=name, str2=hotel_name)
            # print(hotel_name)
            # print(similarity_score)
            if distance < 0.10:
                selected_hotel = accommodation
                break
            elif similarity_score > 0.30 and distance < max_distance_km:
                if selected_hotel is None or distance < selected_hotel[9]:
                    selected_hotel = accommodation

        if selected_hotel:
            id, name, latitude, longitude, stars, price_range, website, contact_phone, amenities, distance = selected_hotel
            return {
                "ID": id,
                "Name": name,
                "Location": (latitude, longitude),
                "Distance": f"{distance:.2f} km",
                "Stars": stars,
                "Price Range": price_range,
                "Website": website,
                "Contact Phone": contact_phone,
                "Amenities": amenities
            }
        else:
            return f"No suitable hotel found within {max_distance_km} km of your location."
    
    cursor.close()
    db_connection.close()


if __name__ == "__main__":
    latitude = 28.6008
    longitude = 77.2373
    hotel_name = "The Oberoi, New Delhi"

    result = find_best_accommodation(latitude, longitude, hotel_name)

    if isinstance(result, dict):
        for key, value in result.items():
            print(f"{key}: {value}")
    else:
        print(result)
