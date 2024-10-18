# WeatherRPC
A Discord Rich Presence that displays the current weather for a specific city. Requires Python and the Discord desktop client.

### Setting up 🔧
1. **Download the source code**: [Click here to download](https://github.com/iakzs/WeatherRPC/archive/refs/heads/main.zip)
2. **Install dependencies**:
   - Open a terminal or command prompt in the project folder.
   - Run the following command to install the required Python packages:
     ```
     pip install -r requirements.txt
     ```
3. **Create a Discord Application**:
   - Go to [Discord Developer Portal](https://discord.com/developers/applications) and create a new application.
   - Give it a meaningful name (e.g., "Weather") as this will be visible in your Discord status.
4. **Get your Client ID**:
   - On the left sidebar, click on "OAuth2" and copy the "Client ID" shown. Save it for later use.
5. **Edit the Script**:
   - Open `main.py` in a text editor or IDE.
   - Replace the `client_id` and any other required variables (like location) with your own information. Ensure that the values are enclosed in quotes, like `'Chicago/United States'`.
6. **Run the Script**:
   - Save your changes and run the script.
7. **Keep Discord Running**:
   - Make sure the Discord desktop client is running for the presence to update.
     
And done!
