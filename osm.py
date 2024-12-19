import requests

def get_osm_details(place_names):
    # Define the Overpass API endpoint
    OVERPASS_URL = "http://overpass-api.de/api/interpreter"
    
    # Build the Overpass query
    def build_query(place_name):
        return f"""
        [out:json];
        (node["name"="{place_name}"];
         way["name"="{place_name}"];
         relation["name"="{place_name}"];);
        out body;
        """
    
    # Function to get details from OSM for a given place
    def fetch_osm_data(place_name):
        query = build_query(place_name)
        response = requests.get(OVERPASS_URL, params={'data': query})
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            return None
    
    # Iterate over the list of places and get data
    place_details = {}
    for place_name in place_names:
        osm_data = fetch_osm_data(place_name)
        if osm_data:
            place_details[place_name] = osm_data
        else:
            place_details[place_name] = f"Details for {place_name} not found in OSM."
    
    return place_details

# List of places from the itinerary
places = [
    "Eiffel Tower",
    "Champ de Mars",
    "Seine River",
    "Louvre Museum",
    "Le Marais",
    "Arc de Triomphe",
    "Champs-Élysées",
    "Montmartre",
    "Sacré-Cœur Basilica",
    "Saint-Germain-des-Prés"
]

# Get details for each place
place_info = get_osm_details(places)

# Print the results
for place, info in place_info.items():
    print(f"Details for {place}:")
    print(info)
    print("\n" + "-"*50 + "\n")
