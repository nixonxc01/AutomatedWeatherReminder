import requests
import googlemaps
import os
from dotenv import load_dotenv

load_dotenv(dotenv_path='env')

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_WEATHER_ENDPOINT = os.getenv('GOOGLE_WEATHER_ENDPOINT')

gmaps = googlemaps.Client(key=GOOGLE_API_KEY)

#Getting user location and converting it to LAT/LON VIA GMAPS
user_location = input('Please enter location: ')
geocode_result = gmaps.geocode(user_location)
LATITUDE = geocode_result[0]['geometry']['location']['lat']
LONGITUDE = geocode_result[0]['geometry']['location']['lng']


weather_parameter = {
    'key':GOOGLE_API_KEY,
    'location.latitude':LATITUDE,
    'location.longitude':LONGITUDE,
    'hours':'16'
}

weather_response = requests.get(GOOGLE_WEATHER_ENDPOINT,params=weather_parameter)
weather_response.raise_for_status()
weather_data = weather_response.json()
rain = 0
for i in range(16):
    weather_condition = weather_data['forecastHours'][i]['precipitation']['probability']['type']
    if weather_condition == 'RAIN':
        rain+=1
if rain >= 1:
    print('Bring umbrella')





