from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

import aqi

app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)
    sender = request.values.get('From', None)

    # Start our TwiML response
    resp = MessagingResponse()

    if 'Hi' in body:
        aqi.send_sms(sender)
    else:
        replyText = aqi.getReply(body)
        resp.message(replyText)

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)