from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import config, requests

def getReply(body):
    result = [x.strip() for x in body.split(',')] #split location by commma separated fields
    aqi_url = 'http://api.airvisual.com/v2/city'
    payload = {'city': result[0], 'state': result[1], 'country':result[2], 'key': config.API_KEY}
    response = requests.get(aqi_url, params=payload).json()

    if 'data' in response:
        aqi = response['data']['current']['pollution']['aqius']
        return "The current AQI in " + result[0] + " is " + str(aqi)
    else:
        return "Sorry, something went wrong."

def send_sms():
    client = Client()
    message = client.messages \
        .create(
             body='What city are you in? Ex, Portland, Oregon, USA',
             from_=config.TWILIO_NUMBER,
             to=config.PERSONAL_NUMBER
         )
    #print(message.sid)

send_sms()

app = Flask(__name__)

@app.route("/sms", methods=['GET', 'POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    replyText = getReply(body)

    # Determine the right reply for this message
    # if body == 'hello':
    #     resp.message("Hi!")
    # elif body == 'bye':
    #     resp.message("Goodbye")

    resp.message(replyText)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)