import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define your ImgBB API token
IMGBB_API_KEY = '6f4c3d83f01aab9a400601709348e451'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me an image to upload.')

def upload_image(update: Update, context: CallbackContext) -> None:
    if update.message.photo:
        # Get the file ID of the largest available photo
        file_id = update.message.photo[-1].file_id
        file = context.bot.get_file(file_id)

        # Get the image URL from the Telegram server
        image_url = file.file_path

        # Upload the image URL to ImgBB
        response = requests.post('https://api.imgbb.com/1/upload', data={
            'key': IMGBB_API_KEY,
            'image': image_url
        })

        if response.status_code == 200:
            imgbb_response = response.json()
            image_url = imgbb_response['data']['url']
            update.message.reply_text(f"Image uploaded! Here's the link: {image_url}")
        else:
            update.message.reply_text("Sorry, something went wrong while uploading the image.")
    else:
        update.message.reply_text("Please send an image to upload.")

def main() -> None:
    # Create the Updater and pass your bot token
    updater = Updater("6370335966:AAEnZfdJ2FD2EJE7dlFg1LI9XIyH5VfmSgU")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command and message handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, upload_image))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you send a signal to stop
    updater.idle()

if __name__ == '__main__':
    main()
