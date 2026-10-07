from django import forms
from django.utils import timezone

from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name', 'amount', 'category', 'payment_method', 'expense_date', 'comment']
        widgets = {
            'expense_date': forms.DateInput(attrs={'type': 'date'}),
            'comment': forms.Textarea(attrs={'rows': 4}),
        }

    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if len(name) < 3:
            raise forms.ValidationError('Название должно содержать минимум 3 символа.')
        return name

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError('Сумма должна быть больше нуля.')
        return amount

    def clean_expense_date(self):
        expense_date = self.cleaned_data['expense_date']
        if expense_date > timezone.localdate():
            raise forms.ValidationError('Дата расхода не может быть в будущем.')
        return expense_date
