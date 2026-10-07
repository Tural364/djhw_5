from django.contrib import admin

from .models import Expense


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', 'category', 'payment_method', 'expense_date', 'owner', 'created_at')
    list_filter = ('category', 'payment_method', 'expense_date')
    search_fields = ('name', 'comment', 'owner__username')
    list_select_related = ('owner',)
    readonly_fields = ('created_at',)
