from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExpenseForm
from .models import Expense


@login_required
def expense_list(request):
    expenses = Expense.objects.filter(owner=request.user)

    q = request.GET.get('q', '').strip()
    category = request.GET.get('category', '')
    payment_method = request.GET.get('payment_method', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')

    if q:
        expenses = expenses.filter(name__icontains=q)
    if category:
        expenses = expenses.filter(category=category)
    if payment_method:
        expenses = expenses.filter(payment_method=payment_method)
    if date_from:
        try:
            expenses = expenses.filter(expense_date__gte=date.fromisoformat(date_from))
        except ValueError:
            date_from = ''
    if date_to:
        try:
            expenses = expenses.filter(expense_date__lte=date.fromisoformat(date_to))
        except ValueError:
            date_to = ''

    total_amount = expenses.aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

    context = {
        'expenses': expenses,
        'categories': Expense.Category.choices,
        'payment_methods': Expense.PaymentMethod.choices,
        'filters': {
            'q': q,
            'category': category,
            'payment_method': payment_method,
            'date_from': date_from,
            'date_to': date_to,
        },
        'count': expenses.count(),
        'total_amount': total_amount,
    }
    return render(request, 'expenses/expense_list.html', context)


@login_required
def expense_detail(request, pk):
    expense = get_object_or_404(Expense, pk=pk, owner=request.user)
    return render(request, 'expenses/expense_detail.html', {'expense': expense})


@login_required
def expense_create(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.owner = request.user
            expense.save()
            messages.success(request, 'Расход успешно добавлен.')
            return redirect('expense_detail', pk=expense.pk)
    else:
        form = ExpenseForm(initial={'expense_date': date.today()})

    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Добавить расход'})


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, owner=request.user)

    if request.method == 'POST':
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            messages.success(request, 'Расход успешно изменён.')
            return redirect('expense_detail', pk=expense.pk)
    else:
        form = ExpenseForm(instance=expense)

    return render(request, 'expenses/expense_form.html', {'form': form, 'title': 'Редактировать расход'})


@login_required
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk, owner=request.user)

    if request.method == 'POST':
        expense.delete()
        messages.success(request, 'Расход успешно удалён.')
        return redirect('expense_list')

    return render(request, 'expenses/expense_confirm_delete.html', {'expense': expense})


def register(request):
    if request.user.is_authenticated:
        return redirect('expense_list')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация выполнена. Добро пожаловать!')
            return redirect('expense_list')
    else:
        form = UserCreationForm()

    return render(request, 'registration/register.html', {'form': form})
