from twilio.rest import Client
#from dotenv import load_dotenv #dev env only
import requests, states, os

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

def send_sms(sender):
    message = client.messages \
        .create(
             body='Hello, I\'m AirQualityBot. What city are you in? Ex. Portland, OR',
             from_=os.getenv('TWILIO_NUMBER'),
             to=sender
         )
    print(message.sid)

def getReply(body):
	result = [x.strip() for x in body.split(',')] #parse location
	aqi_url = 'http://api.airvisual.com/v2/city'
	API_KEY = os.getenv('API_KEY')

	if len(result[1]) == 2: #convert state abbreviation from CA->California for API
		result[1] = result[1].upper() #capitalize ca -> CA for state lookup
		result[1] = states.us_state_abbrev[result[1]]

	location = {'city': result[0], 'state': result[1], 'country':'USA', 'key': API_KEY}
	response = requests.get(aqi_url, params=location).json()

	if 'success' in response['status']:
		aqi = response['data']['current']['pollution']['aqius']
		return "The current AQI in "+response['data']['city']+" is "+str(aqi)+" - "+classify(aqi)
	else:
		return "Sorry, try a different city."

def classify(aqi):
	if aqi<50:
		return "Good"
	elif 51<aqi<100:
		return "Moderate"
	elif 101<aqi<150:
		return "Unhealthy for Sensitive Groups"
	elif 151<aqi<200:
		return "Unhealthy"
	elif 201<aqi<300:
		return "Very Unhealthy"
	elif aqi>301:
		return "Hazardous"
	else:
		return "Invalid aqi"
