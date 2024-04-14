import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

IMGBB_API_KEY = '6f4c3d83f01aab9a400601709348e451'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Send me an image to upload.')

def upload_image(update: Update, context: CallbackContext) -> None:
    if update.message.photo:

        file_id = update.message.photo[-1].file_id
        file = context.bot.get_file(file_id)
        image_url = file.file_path
        response = requests.post('https://api.imgbb.com/1/upload', data={
            'key': IMGBB_API_KEY,
            'image': image_url
        })

        if response.status_code == 200:
            imgbb_response = response.json()
            image_url = imgbb_response['data']['url']
            update.message.reply_text(f"Image uploaded! Here's the link: <code>{image_url}</code>",
                                      parse_mode='Markdown')
        else:
            update.message.reply_text("Sorry, something went wrong while uploading the image.")
    else:
        update.message.reply_text("Please send an image to upload.")

def main() -> None:
    updater = Updater("6370335966:AAEnZfdJ2FD2EJE7dlFg1LI9XIyH5VfmSgU")
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.photo, upload_image))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
