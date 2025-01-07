import mysql.connector
from mysql.connector import Error
import math
from dotenv import load_dotenv
import os

load_dotenv()

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate the distance between two coordinates using the Haversine formula."""
    R = 6371  
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    return R * c


def fetch_country_info(osmid):
    print(osmid)
    try:
        
        connection = mysql.connector.connect(
            host=os.getenv('host'),
            user=os.getenv('user'),
            password=os.getenv('password'),
            database=os.getenv('database')
        )

        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)

            query = f"""
SELECT * FROM {os.getenv('table_name')} 
WHERE city = %s OR city LIKE %s
"""
            city_name = osmid  # Assuming `osmid` contains the city name
            like_pattern = f"%{city_name}%"

            cursor.execute(query, (city_name, like_pattern))
            # cursor.execute(query, (osmid,))

            results = cursor.fetchall()
            # print(results)
            return results

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return None

    finally:
        
        if connection.is_connected():
            cursor.close()
            connection.close()


if __name__ == "__main__":
    osmid = "paris"  

    results = fetch_country_info(osmid)

    if results:
        reference_lat = 48.86  
        reference_lon = 2.31   

        min_distance = float("inf")
        closest_row = None

        for row in results:
            distance = calculate_distance(
                lat1=reference_lat,
                lon1=reference_lon,
                lat2=row["lat"],
                lon2=row["lon"]
            )
            if distance < min_distance:
                min_distance = distance
                closest_row = row

        if closest_row:
            print("Closest location:", closest_row)
            print("Minimum distance:", min_distance)
    else:
        print("No data found or an error occurred.")
