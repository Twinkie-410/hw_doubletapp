from django.core.exceptions import ValidationError
from django.db import models

from app.internal.models.user import User


def validate_bic(bic):
    # validation should be more difficult see https://www.banki.ru/wikibank/bankovskiy_identifikatsionnyiy_kod_bik/
    if len(str(bic)) != 9:
        raise ValidationError("The length of the bic must be 9")


def validate_card_number(number):
    # validation should be more difficult see https://www.raiffeisen.ru/wiki/nomer-karty-bankovskoj/
    if len(str(number)) != 16:
        raise ValidationError("The length of the bic must be 16")


def number_validator(number: str):
    # current and correspondent number account should be more difficult
    # see https://fincult.info/article/chto-oznachayut-bankovskie-rekvizity-i-zachem-oni-nuzhny/
    if len(number) != 20:
        raise ValidationError("The length of the number must be 20")
    if not number.isnumeric():
        raise ValidationError("This is not number, must be number")


class BankAccount(models.Model):
    cash = models.PositiveIntegerField(default=0)
    bank_name = models.CharField(max_length=255)
    bic = models.PositiveIntegerField(validators=[validate_bic])
    account_number = models.CharField(max_length=20, validators=[number_validator])
    correspondent_number = models.CharField(max_length=20, validators=[number_validator])
    user = models.ForeignKey(User, models.CASCADE)


class Card(models.Model):
    number = models.PositiveBigIntegerField(validators=[validate_card_number])
    limit = models.PositiveIntegerField(default=0)
    bank_account = models.ForeignKey(BankAccount, models.CASCADE)
