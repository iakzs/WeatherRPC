# WeatherRPC
A Discord Rich Presence to show current weather in a city. Requires py and the desktop discord client.
### Setting up 🔧
1. Clone GitHub repo
2. Open a terminal shell in the folder and run `pip install -r requirements.txt`
3. Go to https://www.weatherapi.com/signup.aspx and make an account. After logging in at the start of the page you will find an API Key. Save it somewhere.
4. Go to https://discord.com/developers/applications/ and make a new application. Name it something nice (e.g. Weather) as it will show up in your status.
5. To the left, click on OAuth2 and you will see the client secret. Save it somewhere.
6. Open main.py in a text editor or an IDE. Locate this section:

![image](https://github.com/MakerOfMoon/WeatherRPC/assets/99389504/9336db55-97b9-4001-b25e-4fec5a4eab2b)

8. Replace the client id and variables while leaving them in the ''
9. Add your location by replacing the CITY/COUNTRY. It should look something like this: `'Rome/Italy'`. This data is private.
10. Save the script and run it
11. Done!
