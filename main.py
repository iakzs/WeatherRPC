import time
import requests
from pypresence import Presence
from datetime import datetime
from datetime import date

# DATA TO INPUT
api_key = 'WEATHER API KEY HERE'
client_id = 'YOUR CLIENT ID'
location = 'CITY/COUNTRY'

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = date.today()

RPC = Presence(client_id)
RPC.connect()

def get_weather_data():
    url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={location}&aqi=no'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        weather_data = {
            'temp_c': data['current']['temp_c'],
            'mintemp_c': data['forecast']['forecastday'][0]['day']['mintemp_c'],
            'maxtemp_c': data['forecast']['forecastday'][0]['day']['maxtemp_c'],
            'avgtemp_c': data['forecast']['forecastday'][0]['day']['avgtemp_c'],
            'will_it_rain': data['forecast']['forecastday'][0]['day']['daily_will_it_rain']
        }
        return weather_data
    else:
        return None

def update_discord_rpc():
    while True:
        weather_data = get_weather_data()
        
        if weather_data is not None:
            RPC.update(
                state=f"temp: {weather_data['temp_c']}°C, range: {weather_data['mintemp_c']}-{weather_data['maxtemp_c']}°C",
                details=f"avg: {weather_data['avgtemp_c']}°C | it {'do be raining' if weather_data['will_it_rain'] else 'aint raining'}",
                large_image='clouds',
                large_text='Weather'
            )
            print("data fetched successfully and status updated @", today, current_time, "reupdate in 25m")
        else:
            RPC.update(
                state='please notify moon',
                details='could not fetch data',
                large_image='error', 
                large_text='Error'
            )
            print("could not fetch weather data. please check your internet connection and weather api key @", today, current_time, "retrying in 25m")
        
        time.sleep(1500)

if __name__ == '__main__':
    update_discord_rpc()
