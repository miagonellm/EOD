import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route('/api/chat', methods=['POST'])
def chat():
    # Get API key from environment
    api_key = os.getenv('GROK_API_KEY')
    
    if not api_key:
        return jsonify({'error': 'API key not configured'}), 500
    
    # Get message from frontend
    data = request.json
    user_message = data.get('message', '')
    
    # Call Grok API
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }
    
    body = {
        'model': 'grok-3-mini',
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': user_message}
        ],
        'temperature': 0.9,
        'max_tokens': 2000
    }
    
    response = requests.post(
        'https://api.x.ai/v1/chat/completions',
        headers=headers,
        json=body
    )
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(debug=True, port=5000)
