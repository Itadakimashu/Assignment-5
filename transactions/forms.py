from django import forms
from .models import Transaction

from accounts.models import UserBankAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account') # account value ke pop kore anlam
        super().__init__(*args, **kwargs)
        self.fields['transaction_type'].disabled = True # ei field disable thakbe
        self.fields['transaction_type'].widget = forms.HiddenInput() # user er theke hide kora thakbe

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):
    def clean_amount(self): # amount field ke filter korbo
        min_deposit_amount = 100
        amount = self.cleaned_data.get('amount') # user er fill up kora form theke amra amount field er value ke niye aslam, 50
        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = 500
        max_withdraw_amount = 20000
        balance = account.balance # 1000
        amount = self.cleaned_data.get('amount')
        if amount < min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )

        if amount > max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )

        if amount > balance: # amount = 5000, tar balance ache 200
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )
        
        if account.bank.bankrupt:
            raise forms.ValidationError(
                f'The Bank has gone Bankrupt'
            )

        return amount



class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        amount = self.cleaned_data.get('amount')

        return amount
    

class TransferForm(TransactionForm):
    class Meta:
        model = Transaction
        fields = ['amount','transfer_account_number', 'transaction_type']


    def clean_amount(self):
        min_amount_transfer = 500
        max_amount_transfer = 500000
        amount = self.cleaned_data.get('amount')
        account = self.account
        if amount < min_amount_transfer:
            raise forms.ValidationError(f'You can transfer at least {min_amount_transfer} $')
    
        if amount > max_amount_transfer:
            raise forms.ValidationError(f'You can transfer at most {max_amount_transfer} $')
        
        if amount > account.balance:
            raise forms.ValidationError(f'You have {account.balance} $ in your account. You can not transfer more than your account balance')
        
        return amount
    
    def clean_transfer_account_number(self):
        transfer_account_number = self.cleaned_data.get('transfer_account_number')
        try:
            account = UserBankAccount.objects.get(account_no=transfer_account_number)
        except UserBankAccount.DoesNotExist:
            raise forms.ValidationError('Invalid account number. Account does not exist.')
        return transfer_account_number