import os
from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_API_URL = "https://api.geminipro.com/v1/chat"

def query_gemini(question):
    headers = {
        "Authorization": f"Bearer {GEMINI_API_KEY}",
        "Content-Type": "application/json",
    }
    data = {
        "prompt": question,
        "max_tokens": 100,  # You can adjust this based on API documentation
        "temperature": 0.5  # Adjust this for creative vs. factual responses
    }
    response = requests.post(GEMINI_API_URL, json=data, headers=headers)
    return response.json()

@app.route("/chat", methods=["POST"])
def chat():
    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"error": "No question provided"}), 400
    
    # Call the Gemini Pro API
    gemini_response = query_gemini(user_question)
    
    # Parse and return the API's response
    bot_reply = gemini_response.get("choices", [{}])[0].get("text", "Sorry, I didn't understand.")
    
    return jsonify({"response": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
