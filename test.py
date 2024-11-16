# test.py - Simulate the behavior of your API using a test message
import requests

# Simulate a message indicating someone is trying to sell tickets
message_data = {
    "text": "I want to sell my concert tickets!",
    "sender_id": "123456789",
    "user_id": "123456789",
    "bot_id": "98532149a4a0f31e89754bb578"
}

response = requests.post('http://localhost:5001/groupme-callback', json=message_data)
print(response.status_code)
print(response.text)