from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API key from Render environment variables
API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = API_KEY

@app.route('/salesiq-webhook', methods=['POST', 'HEAD'])
def salesiq_webhook():
    # Handle HEAD request (SalesIQ validation)
    if request.method == 'HEAD':
        return '', 200  # Respond with 200 OK for webhook activation

    try:
        # Get the JSON data from SalesIQ webhook
        data = request.json  
        user_message = data.get("visitor_question", "Hello!")

        # Debugging: Log received data
        print(f"Received question: {user_message}")

        # Call OpenAI GPT API
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful chatbot that provides support."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract chatbot reply
        bot_reply = response.choices[0].message.content

        # Debugging: Log OpenAI response
        print(f"Bot Reply: {bot_reply}")

        return jsonify({"reply": bot_reply})

    except Exception as e:
        print(f"Error: {str(e)}")  # Log error
        return jsonify({"reply": "I am experiencing issues. Please try again later."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
