import json
from functools import wraps
from django.core.exceptions import ValidationError
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.forms import model_to_dict
from django.http import JsonResponse
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from phonenumber_field.validators import validate_international_phonenumber
from app.internal.models.user import User
from app.internal.services.user_service import UserSerializer


def check_phone(func):
    @wraps(func)
    async def wrapped(update: Update, context: ContextTypes.DEFAULT_TYPE):
        try:
            user = await User.objects.aget(external_id=update.message.from_user.id)
        except User.DoesNotExist:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Мы не смогли найти ваши данные, пожалуйста, запустите команду /start")
            return

        if user.phone == '':
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="Команда не доступна. Пожалуйста, введите номер '/set_phone номер', чтобы разблокировать все возможности бота")
            return

        await func(update, context)

    return wrapped


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user, _ = await User.objects.aget_or_create(
        external_id=update.message.from_user.id,
        defaults={
            'first_name': update.message.from_user.first_name,
            'username': update.message.from_user.username,
            'phone': '',
        }
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


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

    user, _ = await User.objects.aupdate_or_create(
        external_id=update.message.from_user.id,
        defaults={
            'first_name': update.message.from_user.first_name,
            'username': update.message.from_user.username,
            'phone': phone,
        }
    )

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
    user = await User.objects.aget(external_id=update.message.from_user.id)
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=str(UserSerializer(user).data))


async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")


start_handler = CommandHandler('start', start)
personal_info_handler = CommandHandler('me', me)
echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), echo)
caps_handler = CommandHandler('caps', caps)
set_phone_handler = CommandHandler('set_phone', set_phone)
unknown_handler = MessageHandler(filters.COMMAND, unknown)
