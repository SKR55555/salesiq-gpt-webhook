from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API Key
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

@app.route('/salesiq-webhook', methods=['POST', 'HEAD'])
def salesiq_webhook():
    if request.method == 'HEAD':
        # HEAD request required by Zoho SalesIQ for webhook activation
        return '', 200

    try:
        # Get JSON data from Zoho SalesIQ webhook request
        data = request.json  
        user_message = data.get("visitor_question", "Hello!")

        # Call OpenAI GPT with the user message
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot that provides support."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract AI response
        bot_reply = response["choices"][0]["message"]["content"]

        # Zoho SalesIQ expects a "responses" array with a "text" type response
        salesiq_response = {
            "responses": [
                {
                    "type": "text",
                    "text": bot_reply
                }
            ]
        }

        return jsonify(salesiq_response)

    except Exception as e:
        # If OpenAI API fails, return a default structured response
        error_response = {
            "responses": [
                {
                    "type": "text",
                    "text": "I am experiencing technical issues. Please try again later."
                }
            ]
        }
        return jsonify(error_response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
