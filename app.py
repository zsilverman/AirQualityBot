from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse

import aqi

app = Flask(__name__)

@app.route("/sms", methods=['POST'])
def incoming_sms():
    """Send a dynamic reply to an incoming text message"""
    # Get the message the user sent our Twilio number
    body = request.values.get('Body', None)

    # Start our TwiML response
    resp = MessagingResponse()

    if 'Hi' in body: #or 'hi' or 'Hello' or 'Hi': #body != 'hello' or 'hi' or 'Hello' or 'Hi': 
        aqi.send_sms()
    else:
        replyText = aqi.getReply(body)
        resp.message(replyText)
    #else:
    #    resp.message('Please say \"Hi\" or \"Hello\" to get started')

    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)