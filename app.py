from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Aircall API credentials
aircall_api_token = "12cce349c40d99eca79b4cc0f3f5c275"

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    try:
        # Parse incoming JSON payload from Make.com
        payload = request.json
        
        # Forward payload to Aircall
        aircall_url = 'https://api.aircall.io/v1/webhooks'
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {aircall_api_token}'
        }
        response = requests.post(aircall_url, json={'data': payload}, headers=headers)
        
        if response.ok:
            return jsonify({'status': 'success', 'message': 'Webhook forwarded to Aircall successfully'}), 200
        else:
            return jsonify({'status': 'error', 'message': 'Failed to forward webhook to Aircall'}), 500
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
