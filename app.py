from flask import Flask, request, jsonify
import requests
import openai
import os
import subprocess  # Import the subprocess module to run scripts

app = Flask(__name__)

BOT_ID = "98532149a4a0f31e89754bb578"

# Set OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')  # Use environment variable for security

# Function to check if a message is about buying or selling tickets using OpenAI
def is_ticket_related(message):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Is the following message trying to buy or sell tickets: '{message}'?",
        max_tokens=5
    )
    result = response.choices[0].text.strip().lower()
    return "yes" in result

# Function to send a message back to GroupMe
def send_groupme_message(text):
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": BOT_ID,
        "text": text
    }
    requests.post(url, json=data)

# Function to kick a user from the GroupMe chat
def kick_user_from_groupme(user_id):
    url = f"https://api.groupme.com/v3/groups/{GROUP_ID}/members/{user_id}/remove"
    data = {
        "bot_id": BOT_ID
    }
    response = requests.post(url, json=data)
    return response.json()

# Endpoint for receiving messages from GroupMe
@app.route('/groupme-callback', methods=['POST'])
def groupme_callback():
    data = request.json
    message_text = data['text']
    sender_id = data['sender_id']
    user_id = data['user_id']  # Assuming user_id is provided in the incoming message payload

    # Ignore messages from the bot itself to avoid loops
    if sender_id == BOT_ID:
        return "Message from the bot; ignoring", 200

    # Check if the message is related to tickets using OpenAI
    if is_ticket_related(message_text):
        send_groupme_message(f"User {sender_id}, I noticed you're trying to sell tickets. You will be removed.")
        kick_user_from_groupme(user_id)  # Kick the user from the group
        return "OK, user removed.", 200
    
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)