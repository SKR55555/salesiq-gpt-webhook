from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Load OpenAI API Key from environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")  

@app.route('/salesiq-webhook', methods=['POST'])
def salesiq_webhook():
    try:
        # Get the JSON data from Zoho SalesIQ webhook request
        data = request.json  
        user_message = data.get("visitor_question", "Hello!")  

        # Call OpenAI GPT with the user message
        response = openai.chat.completions.create(
            model="gpt-4",  # Change to 'gpt-3.5-turbo' if needed
            messages=[
                {"role": "system", "content": "You are a helpful chatbot that provides support."},
                {"role": "user", "content": user_message}
            ]
        )

        # Extract response
        bot_reply = response.choices[0].message.content

        # Return the response to Zoho SalesIQ
        return jsonify({"reply": bot_reply})

    except Exception as e:
        return jsonify({"reply": f"Error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
