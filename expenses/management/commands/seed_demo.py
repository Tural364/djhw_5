from datetime import date, timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from expenses.models import Expense


class Command(BaseCommand):
    help = 'Создаёт двух пользователей и по пять расходов для каждого.'

    def handle(self, *args, **options):
        users_data = [
            ('tural', 'tural12345'),
            ('student', 'student12345'),
        ]

        expenses = [
            ('Продукты', 'food', 'card', '18.50'),
            ('Автобус', 'transport', 'cash', '1.00'),
            ('Курс Python', 'education', 'card', '35.00'),
            ('Кино', 'entertainment', 'card', '12.00'),
            ('Аптека', 'health', 'cash', '8.50'),
        ]

        for username, password in users_data:
            user, created = User.objects.get_or_create(username=username)
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(self.style.SUCCESS(f'Создан пользователь: {username}'))
            else:
                self.stdout.write(f'Пользователь уже существует: {username}')

            for index, (name, category, payment_method, amount) in enumerate(expenses):
                Expense.objects.get_or_create(
                    owner=user,
                    name=name,
                    defaults={
                        'amount': Decimal(amount),
                        'category': category,
                        'payment_method': payment_method,
                        'expense_date': date.today() - timedelta(days=index),
                        'comment': 'Демо-запись',
                    },
                )

        self.stdout.write(self.style.SUCCESS('Демо-данные готовы.'))
