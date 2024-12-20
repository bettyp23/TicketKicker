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

# Function to run the external script when a ticket-related message is detected
def run_ticket_script():
    subprocess.run(['python3', 'ticket_script.py'])  # Adjust the script name if needed

# Function to send a message back to GroupMe
def send_groupme_message(text):
    url = "https://api.groupme.com/v3/bots/post"
    data = {
        "bot_id": BOT_ID,
        "text": text
    }
    requests.post(url, json=data)

# Endpoint for receiving messages from GroupMe
@app.route('/groupme-callback', methods=['POST'])
def groupme_callback():
    data = request.json
    message_text = data['text']
    sender_id = data['sender_id']

    # Ignore messages from the bot itself to avoid loops
    if sender_id == BOT_ID:
        return "Message from the bot; ignoring", 200

    # Check if the message is related to tickets using OpenAI
    if is_ticket_related(message_text):
        print(f"OpenAI response: ")  # Add this line
        run_ticket_script()  # Run the external script
        send_groupme_message("Got it! I'll help you with the ticket.")  # Send a confirmation message
    
    return "OK", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)


#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