import json
import re


def parse_itinerary2(text):
    itinerary = {}
    destinations = set()

    # Split the text into days using regex for <dayX> tags
    days = re.split(r'<day(\d+)>', text)

    for i in range(1, len(days), 2):
        day_number = int(days[i])
        day_content = days[i + 1].strip()
        itinerary[f"day{day_number}"] = []

        # Extract time blocks and their descriptions
        for match in re.finditer(r'<(\d+-\d+)> (.+?)(?=(<\d+-\d+>|</day\d+>))', day_content, re.DOTALL):
            time_range = match.group(1)
            description = match.group(2).strip()

            # Extract places, cuisines, and destinations if mentioned
            places = re.findall(r'<PLACE>(.*?)</PLACE>', description)
            cuisines = re.findall(r'<CUISINE>(.*?)</CUISINE>', description)
            local_destinations = re.findall(r'<DESTINATION>(.*?)</DESTINATION>', description)
            # print(local_destinations)
            # Collect destinations
            destinations.update(places + local_destinations)

            # Clean the description by removing tags
            clean_description = re.sub(r'<(/?PLACE|/?CUISINE|/?DESTINATION)>', '', description).strip()

            activity = {
                "time": time_range,
                "description": clean_description,
                "places": places,
                "cuisines": cuisines
            }
            itinerary[f"day{day_number}"].append(activity)

    with open("itenary.json", "w") as f:
        json.dump(itinerary, f, indent=4)
    print(destinations)
    # Return both the itinerary and the destinations
    return {
        "itinerary": json.dumps(itinerary, indent=4),
        "destinations": sorted(destinations)
    }




def parse_itinerary(text):
    itinerary = {}

    # Split the text into days using regex for <dayX> tags
    days = re.split(r'<day(\d+)>', text)

    for i in range(1, len(days), 2):
        day_number = int(days[i])
        day_content = days[i + 1].strip()
        itinerary[f"day{day_number}"] = []

        # Extract time blocks and their descriptions
        for match in re.finditer(r'<(\d+-\d+)> (.+?)(?=(<\d+-\d+>|</day\d+>))', day_content, re.DOTALL):
            time_range = match.group(1)
            description = match.group(2).strip()

            # Extract places and cuisines if mentioned
            places = re.findall(r'<PLACE>(.*?)</PLACE>', description)
            cuisines = re.findall(r'<CUISINE>(.*?)</CUISINE>', description)

            # Clean the description by removing tags
            clean_description = re.sub(r'<(/?PLACE|/?CUISINE)>', '', description).strip()

            activity = {
                "time": time_range,
                "description": clean_description,
                "places": places,
                "cuisines": cuisines
            }
            itinerary[f"day{day_number}"].append(activity)

    return json.dumps(itinerary, indent=4)
if __name__ == "__main__":
# Example Usage
    text = '''<day1>
    <10-11> Arrive at <PLACE>Charles de Gaulle Airport (CDG)</PLACE> and take the RER B train to your hotel in central Paris. Check in to your hotel.
    <11-1> Stroll through the <PLACE>Tuileries Garden</PLACE> towards the <PLACE>Louvre Museum</PLACE>.
    <1-2>  Lunch at a cafe near the Louvre with <CUISINE>classic French bistro fare</CUISINE>.
    <2-4> Visit the <PLACE>Louvre Museum</PLACE> focusing on key masterpieces like the Mona Lisa and Venus de Milo (pre-book tickets!).
    <4-7> Walk along the <PLACE>Seine River</PLACE>, admiring the architecture and bridges.  Enjoy a leisurely dinner at a restaurant in the <PLACE>Saint-Germain-des-Prés</PLACE> district with <CUISINE>French cuisine</CUISINE>.
    <7-9> Evening stroll along the Seine.
    </day1>

    <day2>
    <10-12> Visit the <PLACE>Eiffel Tower</PLACE> (pre-book tickets to avoid long queues). Take the elevator to the top for panoramic views of Paris.
    <12-1> Enjoy a quick <CUISINE>crepe</CUISINE> from a street vendor near the Eiffel Tower.
    <1-3> Visit <PLACE>Les Invalides</PLACE>, including the <PLACE>Army Museum</PLACE> and Napoleon's tomb.
    <3-5>  Explore the charming <PLACE>Latin Quarter</PLACE>, browsing bookstores and soaking in the atmosphere.
    <5-7>  Enjoy a <CUISINE>traditional French dinner</CUISINE> in the Latin Quarter.
    <7-9> Experience a traditional <PLACE>Parisian cabaret show</PLACE> (e.g., Moulin Rouge - book tickets well in advance).

    </day2>

    <day3>
    <10-12> Visit the <PLACE>Sacré-Cœur Basilica</PLACE> in Montmartre. Climb to the top for stunning views of the city.
    <12-1> Explore the artistic streets of <PLACE>Montmartre</PLACE>, including the <PLACE>Place du Tertre</PLACE> where artists create and sell their work.  Grab a quick lunch at a local cafe with <CUISINE>casual French food</CUISINE>.
    <1-3> Visit the <PLACE>Musée d'Orsay</PLACE>, housed in a beautiful former train station, showcasing Impressionist and Post-Impressionist art.
    <3-5> Take a relaxing boat tour on the <PLACE>Seine River</PLACE>.
    <5-7> Enjoy a final Parisian dinner near your hotel with <CUISINE>French food</CUISINE>.
    <7-9> Depart from <PLACE>Charles de Gaulle Airport (CDG)</PLACE>.

    </day3>'''

    print(parse_itinerary(text))
