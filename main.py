# made by github.com/iakzs 
import time
import requests
from pypresence import Presence

# RPC
client_id = '' # add the discord client id
RPC = Presence(client_id)
RPC.connect()

# Weatherapi.com details
api_key = '' # add your api key
location = ''  # add yourcity/country

# 
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
                state=f"Temp: {weather_data['temp_c']}°C, Min: {weather_data['mintemp_c']}°C, Max: {weather_data['maxtemp_c']}°C",
                details=f"Avg Temp: {weather_data['avgtemp_c']}°C, Is it raining: {'Yes' if weather_data['will_it_rain'] else 'No'}",
                large_image='clouds',
                large_text='Weather'
            )
        else:
            RPC.update(
                state='Could not fetch weather data',
                details='hmmm... something went wrong',
                large_image='clouds', 
                large_text='Weather'
            )
        
        time.sleep(30000) # this depends of what plan you have for the api.

if __name__ == '__main__':
    update_discord_rpc()
