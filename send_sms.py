from twilio.rest import Client

client = Client()

def outgoing_text():
	message = client.messages \
	    .create(
	         body='What is your location?',
	         from_='+14154498470',
	         to='+16509956961'
	     )

	print(message.sid)