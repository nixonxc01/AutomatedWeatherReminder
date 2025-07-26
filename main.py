import requests
import googlemaps
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, session

app = Flask(__name__)

load_dotenv(dotenv_path='env')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_WEATHER_ENDPOINT = os.getenv('GOOGLE_WEATHER_ENDPOINT')

def main(location):
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
    print(weather_data['forecastHours'])
    rain = 0
    for i in range(16):
        weather_condition = weather_data['forecastHours'][i]['precipitation']['probability']['type']
        if weather_condition == 'RAIN':
            rain += 1
            print('work1')
        else:
            print('work2')
    if rain >= 1:
        print('Bring umbrella')

@app.route('/',methods=['GET','POST'])
def input_page():
    if request.method == 'POST':
        email = request.form['email']
        location = request.form['location']
        main(location)
    return render_template('smartweather.html')


if __name__ == '__main__':
    app.run(debug=True)

