import discord
import json
from flask import Flask, request, jsonify

app = Flask(__name__)
client = discord.Client()

# Load Discord bot token from config.json
with open('config.json') as f:
    config = json.load(f)
TOKEN = config['token']

# Discord channel ID where you want to send the passport data (replace 'YOUR_CHANNEL_ID' with the actual channel ID)
CHANNEL_ID = 1234567890  # Example channel ID

# Define an event that triggers when the bot is ready
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# Endpoint to receive passport data from the client
@app.route('/passport', methods=['POST'])
def receive_passport():
    passport_data = request.json
    print('Passport data received:', passport_data)
    
    # Send the passport data to the Discord channel
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        # Format the passport data into a message
        message = 'Passport Details:\n'
        for key, value in passport_data.items():
            message += f'{key}: {value}\n'
        
        # Send the message to the Discord channel
        await channel.send(message)
        return jsonify({'message': 'Passport sent successfully to Discord'})
    else:
        return jsonify({'error': 'Failed to send passport to Discord'})

if __name__ == '__main__':
    # Start the Flask server
    app.run(debug=True)  # You may need to adjust the host and port

# Run the Discord bot
client.run(TOKEN)
