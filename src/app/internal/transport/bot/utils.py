from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from app.internal.services.user_service import get_user_by_id


def check_phone(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = await get_user_by_id(update.message.from_user.id)
        if not user:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Мы не смогли найти ваши данные, пожалуйста, запустите команду /start")
            return

        if user.phone == '':
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Команда не доступна. Пожалуйста, введите номер '/set_phone номер', чтобы разблокировать все возможности бота")
            return

        await func(update, context)

    return wrapped
