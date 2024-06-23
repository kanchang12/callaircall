from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
import openai
import os

app = Flask(__name__)

# Configure your Twilio and OpenAI API keys here
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_sid")
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_token')
TWILIO_PHONE_NUMBER = '+447822026339'
OPENAI_API_KEY = os.getenv('OPENAI_API_key')

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
openai.api_key = OPENAI_API_KEY

# Define system instructions
SYSTEM_INSTRUCTIONS = "You are a helpful assistant. Talk about weather"

@app.route('/voice', methods=['POST'])
def voice():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/process', method='POST')
    gather.say('Hello, please say something after the beep.')
    response.append(gather)
    return str(response)

@app.route('/process', methods=['POST'])
def process():
    speech_result = request.form['SpeechResult']
    
    # Create a chat completion request
    openai_response = openai.Chat.Completion.create(
        model="gpt-3.5-turbo-16k",
        messages=[
            {"role": "system", "content": SYSTEM_INSTRUCTIONS},
            {"role": "user", "content": speech_result}
        ]
    )
    
    reply = openai_response.choices[0].message['content']

    # Create Twilio VoiceResponse object to respond back
    response = VoiceResponse()

    # Say the AI's response
    response.say(reply)

    # Continue the conversation with Gather
    gather = Gather(input='speech', action='/process', method='POST')
    gather.say('Please say something after the beep.')
    response.append(gather)

    # Redirect to /process to continue listening
    response.redirect('/process')

    return str(response)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
