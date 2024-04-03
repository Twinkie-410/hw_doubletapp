from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from app.internal.services.bank_service import get_bank_accounts_by_user, get_cards_by_user, transfer_money as transfer, \
    get_account_number
from app.internal.transport.bot.utils import check_phone, check_transfer_command


@check_phone
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bank_accounts = await get_bank_accounts_by_user(update.message.from_user.id)
    # [account async for account in
    #              BankAccount.objects.filter(user__external_id=update.message.from_user.id)]
    account_cash = [f'счёт {account.account_number}: {account.cash} осталось' for account in bank_accounts]

    cards = await get_cards_by_user(update.message.from_user.id)
    # for account in bank_accounts:
    #     cards += [card async for card in Card.objects.filter(bank_account__id=account.id)]
    card_limit = [f'карта {card.number}: {card.limit} осталось' for card in cards]

    separator = '\n'
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Остаток средств на ваших счетах\n{separator.join(a_c for a_c in account_cash)}")

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f"Остаток от лимита на ваших картах\n{separator.join(c_l for c_l in card_limit)}")


@check_phone
async def transfer_money(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = await check_transfer_command(update, context)
    if status:
        command_text = update.message.text.split()
        sender_number = await get_account_number(update.message.from_user.username)
        recipient_number = await get_account_number(command_text[1])
        amount = int(command_text[2])
        response = await transfer(sender_number, recipient_number, amount)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


balance_handler = CommandHandler('balance', balance)
transfer_handler = CommandHandler('transfer_money', transfer_money)
