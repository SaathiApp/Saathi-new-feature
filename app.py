from flask import Flask, render_template, request
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
from parse_llm import parse_itinerary, parse_optimized_route, parse_question_answer

# Load environment variables
load_dotenv()

# Configure the API client
genai.configure(api_key=os.getenv('GEMINI_KEY'))

# Initialize Flask app
app = Flask(__name__)

# Route to display the main page and get input
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Extract the user query from the form
        user_query = request.form.get("query")
        budget = request.form.get("budget")
        trip_type = request.form.get("trip_type")
        
        # Read the prompt file and add user input
        with open("prompt.txt", "r", encoding="utf-8") as f:
            prompt = f.read()
        
        # Add user preferences to the prompt if selected
        preferences = {}
        if budget:
            preferences["budget"] = budget
        if trip_type:
            preferences["trip_type"] = trip_type
        
        # Append the user preferences if there are any
        if preferences:
            preferences_str = f'add user preferences: {json.dumps(preferences)}'
            full_prompt = f"{prompt} {user_query} {preferences_str}"
        else:
            full_prompt = f"{prompt} {user_query}"

        # Request to Gemini API
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt, generation_config=genai.GenerationConfig(response_mime_type="application/json"))

        # Parse the response from the API
        response_json = json.loads(response.text)

        if response_json.get("route"):
            answer = parse_optimized_route(response_json)
        elif response_json.get("itinerary"):
            answer = parse_itinerary(response_json)
        else:
            answer = parse_question_answer(response_json)

        # Return the result to the user
        return render_template("index.html", answer=answer)

    return render_template("index.html", answer=None)

if __name__ == "__main__":
    app.run(debug=True)
