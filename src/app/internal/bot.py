import logging
import os
import django
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from transport.bot.user_handlers import start_handler, echo_handler, caps_handler, unknown_handler, set_phone_handler, \
    personal_info_handler, remove_from_favorite_handler, add_to_favorite_handler, check_favorites_handler
from app.internal.transport.bot.bank_handlers import balance_handler, transfer_handler

load_dotenv()
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(os.getenv('TG_TOKEN')).build()

    application.add_handler(start_handler)
    application.add_handler(personal_info_handler)
    application.add_handler(set_phone_handler)
    application.add_handler(echo_handler)
    application.add_handler(caps_handler)
    application.add_handler(balance_handler)
    application.add_handler(transfer_handler)
    application.add_handler(add_to_favorite_handler)
    application.add_handler(remove_from_favorite_handler)
    application.add_handler(check_favorites_handler)
    application.add_handler(unknown_handler)

    application.run_polling()
