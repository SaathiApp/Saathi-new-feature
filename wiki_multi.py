import requests
from bs4 import BeautifulSoup
import wikipedia
from concurrent.futures import ThreadPoolExecutor, as_completed

# Function to get Wikipedia page and extract relevant details
def get_wikipedia_details(page_name):
    try:
        # Get the Wikipedia page object using the page name
        page = wikipedia.page(page_name)

        # Initialize the results dictionary
        result = {
            'summary': page.summary,
            'coordinates': None,
            'official_website': None,
            'photos': []
        }

        # Construct the URL from the page name
        url = page.url

        # Fetch the page content using requests and BeautifulSoup for additional parsing
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract Coordinates from the infobox (typically in the infobox template)
        coordinates = None
        infobox = soup.find('table', {'class': 'infobox'})

        if infobox:
            rows = infobox.find_all('tr')
            for row in rows:
                header = row.find('th')
                if header and 'coordinates' in header.text.lower():
                    coord = row.find('td')
                    if coord:
                        # Extract the coordinates (latitude, longitude)
                        coordinates = coord.text.strip()
                        result['coordinates'] = coordinates

        # Extract official website URL (if available)
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if 'official website' in a_tag.get_text().lower() or 'external link' in a_tag.get_text().lower():
                if href.startswith('http'):
                    result['official_website'] = href
                    break

        # Extract images (photos) from the page
        image_urls = []
        for img_tag in soup.find_all('img'):
            img_url = img_tag.get('src')
            if img_url and img_url.startswith('http'):
                image_urls.append(img_url)

        result['photos'] = image_urls

        if not coordinates:  # Only check for <span> if coordinates weren't found in the infobox
            geo_spans = soup.find_all('span', {'class': 'geo-dec'})
            if geo_spans:
                coordinates = geo_spans[0].text.strip()
                result['coordinates'] = coordinates

        return result

    except wikipedia.exceptions.PageError as e:
        # Handle the case when the page does not exist
        print(f"Page not found: {page_name}")
        return None


# Function to process multiple places in parallel
def process_places_parallel(places):
    # Initialize ThreadPoolExecutor for parallel processing
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(get_wikipedia_details, place) for place in places]

        results = []
        for future in as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
    
    return results


# Example Usage
# places = ["Louvre Museum", "Eiffel Tower", "Great Wall of China","Colosseum"]  # List of places
# details = process_places_parallel(places)

# # Print results for each place
# for place, detail in zip(places, details):
#     print(f"Details for {place}:")
#     if detail:  # Only print details if not None (i.e., page was found)
#         print(f"  Coordinates: {detail['coordinates']}")
#         print(f"  Official Website: {detail['official_website']}")
#         print(f"  Photos: {detail['photos'][:3]}...")  # Print first 3 photos
#     print()
