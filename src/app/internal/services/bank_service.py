from app.internal.models.bank_account import BankAccount, Card


async def get_bank_accounts_by_user(id):
    return [account async for account in
            BankAccount.objects.filter(user__external_id=id)]


async def get_account_number(requisites):
    accounts = [account async for account in BankAccount.objects.filter(account_number=requisites)]
    if len(accounts) == 0:
        accounts = [account async for account in BankAccount.objects.filter(user__username=requisites)]
        if len(accounts) == 0:
            if requisites.isdigit():
                accounts = [account async for account in BankAccount.objects.filter(card__number=requisites)]
                if len(accounts) == 0:
                    return None
            else:
                return None

    return accounts[0].account_number


async def get_cards_by_user(id):
    return [card async for card in Card.objects.filter(bank_account__user__external_id=id)]


async def transfer_money(sender_number: BankAccount.account_number,
                         recipient_number: BankAccount.account_number,
                         amount: int):
    if await check_transfer(sender_number, recipient_number, amount):
        sender = await BankAccount.objects.aget(account_number=sender_number)
        recipient = await BankAccount.objects.aget(account_number=recipient_number)

        sender.cash -= amount
        recipient.cash += amount
        await sender.asave()
        await recipient.asave()
        return "OK"
    else:
        return "ERROR: check requisites and balance"


async def check_transfer(sender_number: BankAccount.account_number,
                         recipient_number: BankAccount.account_number,
                         amount: int):
    sender = [sender async for sender in BankAccount.objects.filter(account_number=sender_number)]
    recipient = [sender async for sender in BankAccount.objects.filter(account_number=recipient_number)]
    if len(sender) == 1 and len(recipient) == 1:
        if sender[0].cash >= amount:
            return True
        else:
            return False
    else:
        return False
