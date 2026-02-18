from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import re
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load Groq API details
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env file")


# Function to call Groq API
def call_groq(prompt):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }

    body = {
        "model": GROQ_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    try:
        response = requests.post(GROQ_URL, json=body, headers=headers, timeout=30)

        if response.status_code != 200:
            return f"API Error: {response.text}"

        data = response.json()
        result = data["choices"][0]["message"]["content"]

        # Remove markdown symbols like ** or __
        result = re.sub(r"[*_]{1,2}", "", result)

        return result

    except Exception as e:
        return f"API error. Please try again. Error: {str(e)}"


# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Generate marketing campaign
@app.route("/generate_campaign", methods=["POST"])
def generate_campaign():
    product = request.form.get("product")
    audience = request.form.get("audience")
    platform = request.form.get("platform")

    prompt = f"""
Generate a detailed marketing campaign.

Product: {product}
Target Audience: {audience}
Platform: {platform}

Include:
- Campaign objective
- Content ideas
- Ad copies
- Call to action
"""

    output = call_groq(prompt)

    return jsonify({"result": output})


# Generate sales pitch
@app.route("/generate_pitch", methods=["POST"])
def generate_pitch():
    product = request.form.get("product")
    customer = request.form.get("customer")

    prompt = f"""
Create a compelling AI sales pitch.

Product: {product}
Customer Persona: {customer}

Include:
- 30-second pitch
- Value proposition
- Key benefits
- Call to action
"""

    output = call_groq(prompt)

    return jsonify({"result": output})


# Lead scoring
@app.route("/score", methods=["POST"])
def lead_score():
    name = request.form.get("name")
    budget = request.form.get("budget")
    need = request.form.get("need")
    urgency = request.form.get("urgency")

    prompt = f"""
Score this lead from 0 to 100 based on Budget, Need, and Urgency.

Lead Name: {name}
Budget: {budget}
Need: {need}
Urgency: {urgency}

Also explain reasoning.
"""

    output = call_groq(prompt)

    return jsonify({"result": output})


# Run app
if __name__ == "__main__":
    app.run(debug=True)
