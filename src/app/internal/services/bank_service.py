from app.internal.models.bank_account import BankAccount, Card
from app.internal.transport.bot.utils import check_phone


async def get_bank_accounts_by_user(id):
    return [account async for account in
            BankAccount.objects.filter(user__external_id=id)]


async def get_cards_by_user(id):
    return [card async for card in Card.objects.filter(bank_account__user__external_id=id)]
