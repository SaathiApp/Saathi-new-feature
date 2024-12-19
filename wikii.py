import requests
from bs4 import BeautifulSoup
import wikipedia

# Function to get Wikipedia page and extract relevant details
def get_wikipedia_details(page_name):
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
    all_images = []

    # Find all the sections that are part of the main content
    img_tags = soup.find_all('a', {'class': 'mw-file-description'})

    for img_tag in img_tags:
        # Inside each anchor tag, find the <img> tag
        img = img_tag.find('img')
         
        # print(img)
        if img:
            img_url = img.get('src')
            height = img.get('height')
            if img_url and height:
                try:
                # Convert height to an integer and check if it's above the threshold
                    height = int(height)
                    if height > 100:  # Only include images that are larger than 100 pixels in height
                        # Ensure the image is part of the article and not an icon or thumbnail
                        if not any(keyword in img_url for keyword in ['logo', 'icon']):
                            all_images.append(img_url)
                except ValueError:
                    # If height is not an integer, we skip the image (or you can set a default check)
                    continue
                # # Ensure the image is part of the article and not an icon or thumbnail
                # if not any(keyword in img_url for keyword in ['logo', 'icon']):
                #     all_images.append(img_url)

    result['photos'] = all_images
    if not coordinates:  # Only check for <span> if coordinates weren't found in the infobox
        geo_spans = soup.find_all('span', {'class': 'geo-dec'})
        if geo_spans:
            coordinates = geo_spans[0].text.strip()
            result['coordinates'] = coordinates
    return result


# Example Usage
page_name = "Eiffel Tower"  # Replace this with any Wikipedia page name
details = get_wikipedia_details(page_name)

# print(f"Summary: {details['summary']}")
print(f"Coordinates: {details['coordinates']}")
print(f"Official Website: {details['official_website']}")
print(f"Photos: {details['photos']}")
