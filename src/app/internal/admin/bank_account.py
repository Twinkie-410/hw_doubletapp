from django.contrib import admin

from app.internal.models.bank_account import BankAccount, Card


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'bank_name', 'account_number')

    @admin.display(ordering='user__external_id', description='user id')
    def get_user(self, obj):
        return obj.user.external_id

    def get_queryset(self, request):
        return super(BankAccountAdmin, self).get_queryset(request).select_related('user')


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('get_user', 'number', 'get_bank_name', 'get_account_number')

    @admin.display(ordering='bank_account__user__external_id', description='user')
    def get_user(self, obj):
        return obj.bank_account.user.external_id

    @admin.display(ordering='bank_account__bank_name', description='bank name')
    def get_bank_name(self, obj):
        return obj.bank_account.bank_name

    @admin.display(ordering='bank_account__account_number', description='account number')
    def get_account_number(self, obj):
        return obj.bank_account.account_number

    def get_queryset(self, request):
        return super(CardAdmin, self).get_queryset(request).select_related('bank_account', 'bank_account__user')
