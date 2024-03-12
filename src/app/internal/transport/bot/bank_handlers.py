from telegram import Update
from telegram.ext import ContextTypes, CommandHandler

from app.internal.services.bank_service import get_bank_accounts_by_user, get_cards_by_user
from app.internal.transport.bot.utils import check_phone


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


balance = CommandHandler('balance', balance)
