from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API Key from Render environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY  # Set OpenAI API key

@app.route('/salesiq-webhook', methods=['POST', 'HEAD'])
def salesiq_webhook():
    if request.method == 'HEAD':
        return '', 200  # ✅ Respond 200 for HEAD requests

    try:
        data = request.json  # Get JSON from SalesIQ request
        user_message = data.get("visitor_question", "Hello!")  # Extract question
        
        # Generate response using OpenAI GPT
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot."},
                {"role": "user", "content": user_message}
            ]
        )
        
        # Extract response text
        bot_reply = response["choices"][0]["message"]["content"]

        # Return response in the correct format for SalesIQ
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": "I am experiencing issues. Please try again later."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
