from dotenv import load_dotenv
import google.generativeai as genai
import os 
# from utils import parse_itinerary2
# from wiki_multi import process_places_parallel
import json
from parse_llm import parse_itinerary, parse_optimized_route, parse_question_answer
load_dotenv()

genai.configure(api_key=os.environ['GEMINI_KEY'])

with open ("prompt.txt", "r",encoding="utf-8") as f:
    prompt = f.read()
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content( prompt + ''' give me an itenary to mumbai for 2 days
''',
generation_config=genai.GenerationConfig(
        response_mime_type="application/json",))
print(response.text)

response_json = json.loads(response.text)

if response_json.get("route"):
    answer = parse_optimized_route(response_json)
elif response_json.get("itinerary"):
    answer = parse_itinerary(response_json)
else:
    answer = parse_question_answer(response_json)

print(answer)
# print(response)
# j = parse_itinerary2(text=response.text)
# details = process_places_parallel(j['destinations'])    
# for place, detail in zip(j['destinations'], details):
#     print(f"Details for {place}:")
#     if detail:  # Only print details if not None (i.e., page was found)
#         print(f"  Coordinates: {detail['coordinates']}")
#         print(f"  Official Website: {detail['official_website']}")
#         print(f"  Photos: {detail['photos'][:3]}...")  # Print first 3 photos
#     print()

