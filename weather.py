import os
import requests
import googlemaps
from dotenv import load_dotenv
from account import app,Account
from twilio.rest import Client

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_WEATHER_ENDPOINT = os.getenv('GOOGLE_WEATHER_ENDPOINT')
load_dotenv(dotenv_path='env')

account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
client = Client(account_sid, auth_token)


def messenger(number):
    message = client.messages.create(
        body = 'Rain Alert: It’s expected to rain today in your area. Don’t forget to bring an umbrella and stay dry!',
        from_ = twilio_phone_number,
        to = number
    )

def main(location,phone_number):
    #Getting user location and converting it to LAT/LON VIA GMAPS
    gmaps = googlemaps.Client(key=GOOGLE_API_KEY)
    geocode_result = gmaps.geocode(location)
    LATITUDE = geocode_result[0]['geometry']['location']['lat']
    LONGITUDE = geocode_result[0]['geometry']['location']['lng']


    weather_parameter = {
        'key': GOOGLE_API_KEY,
        'location.latitude': LATITUDE,
        'location.longitude': LONGITUDE,
        'hours': '16'
        }

    weather_response = requests.get(GOOGLE_WEATHER_ENDPOINT, params=weather_parameter)
    weather_response.raise_for_status()
    weather_data = weather_response.json()
    rain = 0
    for i in range(16):
        weather_condition = weather_data['forecastHours'][i]['precipitation']['probability']['type']
        if weather_condition == 'RAIN':
            rain += 1
    if rain >= 1:
        messenger(phone_number)

with app.app_context():
    users_with_location = Account.query.filter(Account.location.isnot(None),(Account.location != '')).all()

for users in users_with_location:
    main(users.location,users.phone_number)



