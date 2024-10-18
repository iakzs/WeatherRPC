# made by github.com/iakzs and all the contributors
import time
import requests
from pypresence import Presence
from datetime import datetime
from datetime import date

useWeatherApi = False  # Set this to True to use WeatherAPI.com, otherwise it will use Open-Meteo

api_key = 'WEATHER API KEY HERE'  # Required for WeatherAPI.com

client_id = 'YOUR CLIENT ID' # Required for Discord RPC
location = 'City/Country' # Required to fetch for both Open-Meteo and WeatherAPI.com

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
today = date.today()

RPC = Presence(client_id)
RPC.connect()

def get_latitude_longitude(location):
    """Fetch latitude and longitude for a given city/country using Nominatim (OpenStreetMap)."""
    geocoding_url = f"https://nominatim.openstreetmap.org/search?format=json&q={location}"
    
    headers = {
        'User-Agent': 'WeatherRPC/1.1 (github.com/iakzs/WeatherRPC)' # my bad nominatim
    }
    
    response = requests.get(geocoding_url, headers=headers)

    if response.status_code == 200:
        try:
            data = response.json()
            if len(data) > 0:
                latitude = data[0]['lat']
                longitude = data[0]['lon']
                return float(latitude), float(longitude)
            else:
                print("Error: No results found for the location.")
                return None, None
        except requests.exceptions.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return None, None
    else:
        print(f"Error: Received non-200 status code: {response.status_code} with response text: {response.text}")
        return None, None

def get_weather_data():
    latitude, longitude = get_latitude_longitude(location)

    if latitude is None or longitude is None:
        return None

    if useWeatherApi:
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
            print("Error fetching weather data from WeatherAPI.com")
            return None
    else:
        url = f'https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&hourly=temperature_2m,precipitation_probability&daily=temperature_2m_min,temperature_2m_max&timezone=auto'
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            weather_data = {
                'temp_c': data['hourly']['temperature_2m'][0],
                'mintemp_c': data['daily']['temperature_2m_min'][0],
                'maxtemp_c': data['daily']['temperature_2m_max'][0],
                'will_it_rain': data['hourly']['precipitation_probability'][0] > 0
            }
            return weather_data
        else:
            print("Error fetching weather data from Open-Meteo")
            return None
            
def get_weather_icon(weather_data, avg_temps):
    if weather_data['will_it_rain']:
        return 'rain'
    elif avg_temps > 20:
        return 'sun'
    else:
        return 'clouds'

def update_discord_rpc():
    while True:
        weather_data = get_weather_data()
        
        if weather_data is not None:
            avg_temps = (weather_data['mintemp_c'] + weather_data['maxtemp_c']) / 2
            weather_icon = get_weather_icon(weather_data, avg_temps)
            RPC.update(
                state=f"temp: {weather_data['temp_c']}°C, range: {weather_data['mintemp_c']}-{weather_data['maxtemp_c']}°C",
                details=f"avg: {(weather_data['mintemp_c'] + weather_data['maxtemp_c']) / 2:.1f}°C | it {'is raining :(' if weather_data['will_it_rain'] else 'is not raining :D'}",
                large_image=weather_icon,
                large_text='Weather | github.com/iakzs/WeatherRPC'
            )
            print("Data fetched successfully and status updated @", today, current_time, "Reupdate in 25m")
        else:
            RPC.update(
                state='please notify me',
                details='could not fetch data',
                large_image='error', 
                large_text='Error :( | github.com/iakzs/WeatherRPC'
            )
            print("Could not fetch weather data. Please check your connection @", today, current_time, "Retrying in 25m")
        
        time.sleep(1500)

if __name__ == '__main__':
    update_discord_rpc()
