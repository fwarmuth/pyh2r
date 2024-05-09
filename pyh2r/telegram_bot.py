import telebot
import requests
import os
import datetime

from pyh2r.client import upload_audio

# Use environment variable
bot = telebot.TeleBot(os.environ['PYH2R_TELEGRAM_BOT_API_TOKEN'])

def process_audio(file_path):
    try:
        response = upload_audio(file_path)
    except Exception as e:
        return {"read": {'text': f"Could not connect to h2r server.\nError processing audio file {e}"}}
    
    return response.json()

@bot.message_handler(func=lambda message: True, content_types=['voice'])
def handle_audio(message):
    # Download the voice message and store it in a temporary file
    file_info = bot.get_file(message.voice.file_id)
    file = requests.get(f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}')

    # Create dirs
    os.makedirs('uploaded_files', exist_ok=True)

    file_path = 'uploaded_files/temp_audio.ogg'
    # Check if the environment variable is set and is equal to 1
    if os.environ.get('PYH2R_STORE_AUDIO_FILES', '0') == '1':
        # Create a unique temporary file to store the audio.
        file_path = f'uploaded_files/{datetime.datetime.now().strftime("%Y%m%d-%H%M%S")}_temp_audio.ogg'

    # Save the audio file
    with open(file_path, 'wb') as f:
        f.write(file.content)
    
    bot.reply_to(message, "Audio received! Processing...")
    # Process the audio file
    result = process_audio(file_path)

    # Extract the text from the response
    msg = f"{result['read']['text']}"
    
    # Split the message into chunks of 4096 characters
    done = False
    split_size = 4096
    while not done:
        # Split the message into chunks of 4096 characters
        try:
            for i in range(0, len(msg), split_size):
                msg_chunk = msg[i:i + split_size]
                # Send the message chunk
                bot.reply_to(message, msg_chunk)
            done = True
        except Exception as e:
            split_size = split_size/2
            bot.reply_to(message, "Message too long to send. Splitting message into smaller chunks.")


@bot.message_handler(func=lambda message: True)
def echo_message(message):
    # Echo back the received message
    bot.reply_to(message, message.text)

