from functools import wraps

from telegram import Update
from telegram.ext import ContextTypes

from app.internal.services.bank_service import get_bank_accounts_by_user, get_account_number
from app.internal.services.user_service import get_user_by_id, get_user_by_username


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


async def check_transfer_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bank_accounts_sender = await get_bank_accounts_by_user(update.message.from_user.id)
    if len(bank_accounts_sender) == 0:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Не удалось найти ваш счёт")
        return False

    text = update.message.text.split()
    if len(text) == 3:
        recipient_requisites = text[1]

        try:
            int(text[2])
        except ValueError:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Сумма введена некорректно")
            return False

        recipient_number = await get_account_number(recipient_requisites)
        if recipient_number:
            return True

        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Не удалось найти счёт получателя, проверьте данные")
            return False
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Через пробел введите номер карты, счёта или юзернейм получателя, после через пробел введите сумму")
        return False


async def update_favorite(update: Update, context: ContextTypes.DEFAULT_TYPE, action):
    text = update.message.text.split()
    instance_username = update.message.from_user.username
    favorite_username = text[1] if len(text) == 2 else None
    if favorite_username:
        favorite_user = await get_user_by_username(favorite_username)
        if favorite_user:
            try:
                await action(instance_username, favorite_username)
            except Exception as e:
                await context.bot.send_message(chat_id=update.effective_chat.id,
                                               text=f"SYSTEM ERROR: {e}")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Не удалось найти пользователя по указанному username")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Через пробел введите username пользователя")
