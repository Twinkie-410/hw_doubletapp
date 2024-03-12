from django.core.exceptions import ValidationError
from phonenumber_field.validators import validate_international_phonenumber
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters

from app.internal.models.user import User
from app.internal.services.user_service import get_user_by_id, get_or_create, set_phone_number
from app.internal.transport.bot.utils import check_phone


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user, _ = await get_or_create(id=update.message.from_user.id,
                                  first_name=update.message.from_user.first_name,
                                  username=update.message.from_user.username)
    #     await User.objects.aget_or_create(
    #     external_id=update.message.from_user.id,
    #     defaults={
    #         'first_name': update.message.from_user.first_name,
    #         'username': update.message.from_user.username,
    #         'phone': '',
    #     }
    # )
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Hello, {user.first_name}, i'm ready to work")


async def set_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.split()
    phone = text[1] if len(text) == 2 else ''
    if not phone:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="Введите номер телефона через пробел")
        return

    try:
        validate_international_phonenumber(phone)
    except ValidationError as e:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=str(e.message))
        return

    user, _ = await set_phone_number(id=update.message.from_user.id,
                                     number=phone,
                                     first_name=update.message.from_user.first_name,
                                     username=update.message.from_user.username)
    #     await User.objects.aupdate_or_create(
    #     external_id=update.message.from_user.id,
    #     defaults={
    #         'first_name': update.message.from_user.first_name,
    #         'username': update.message.from_user.username,
    #         'phone': phone,
    #     }
    # )

    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Отлично, теперь ваш номер: {user.phone}")


@check_phone
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


@check_phone
async def caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text_caps = ' '.join(context.args).upper()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


@check_phone
async def me(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = await get_user_by_id(update.message.from_user.id)
    user_data = [f'external_id: {user.external_id}',
                 f'first_name: {user.first_name}',
                 f'username: {user.username}',
                 f'phone: {user.phone.as_e164}']
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='\n'.join(u_d for u_d in user_data))


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start)
personal_info_handler = CommandHandler('me', me)
echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
caps_handler = CommandHandler('caps', caps)
set_phone_handler = CommandHandler('set_phone', set_phone)
unknown_handler = MessageHandler(filters.COMMAND, unknown)
