from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API key from Render environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY  # Set OpenAI API key

@app.route('/salesiq-webhook', methods=['POST'])
def salesiq_webhook():
    try:
        # Log incoming request for debugging
        print("Incoming SalesIQ Request:", request.json)

        # Get the JSON data from Zoho SalesIQ webhook request
        data = request.json
        user_message = data.get("visitor_question", "Hello!")

        # Validate input
        if not user_message:
            return jsonify({"reply": "Error: Missing visitor_question"}), 400

        # Call OpenAI GPT with the user message
        response = openai.ChatCompletion.create(
            model="gpt-4",  # You can change this to 'gpt-3.5-turbo' or other models
            messages=[
                {"role": "system", "content": "You are a helpful chatbot that provides support."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract response from OpenAI
        bot_reply = response["choices"][0]["message"]["content"]

        # Return response to Zoho SalesIQ
        return jsonify({"reply": bot_reply})

    except Exception as e:
        print("Error:", str(e))  # Log error to Render logs
        return jsonify({"reply": "I am experiencing issues. Please try again later."}), 500

@app.route('/webhook', methods=['POST'])  
def webhook():
    try:
        # Log incoming request for debugging
        print("Incoming Webhook Request:", request.json)

        # Get JSON data
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({"error": "Invalid request"}), 400

        question = data['question']
        return jsonify({"reply": f"You asked: {question}"})

    except Exception as e:
        print("Error:", str(e))  # Log error to Render logs
        return jsonify({"error": "Something went wrong"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
