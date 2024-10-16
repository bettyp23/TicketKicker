from flask import Flask, request, jsonify

app = Flask(__name__)

# Define a simple route for testing the bot
@app.route('/bot', methods=['POST'])
def bot_response():
    data = request.json
    message_text = data.get('text', '').strip().lower()  # Get the message text
    
    # Simple response logic based on the message content
    if "hello" in message_text:
        response = "Hello! How can I assist you today?"
    elif "oats" in message_text:
        response = "No."
    elif "buy tickets" in message_text:
        response = "I can help you with that! What tickets are you interested in?"
    else:
        response = "I'm not sure how to respond to that."

    return jsonify({"response": response}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
