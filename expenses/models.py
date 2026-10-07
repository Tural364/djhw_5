from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone


class Expense(models.Model):
    class Category(models.TextChoices):
        FOOD = 'food', 'Продукты'
        TRANSPORT = 'transport', 'Транспорт'
        EDUCATION = 'education', 'Обучение'
        ENTERTAINMENT = 'entertainment', 'Развлечения'
        HEALTH = 'health', 'Здоровье'
        OTHER = 'other', 'Другое'

    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Наличные'
        CARD = 'card', 'Карта'

    name = models.CharField('Название', max_length=120)
    amount = models.DecimalField('Сумма', max_digits=10, decimal_places=2)
    category = models.CharField('Категория', max_length=20, choices=Category.choices)
    payment_method = models.CharField('Способ оплаты', max_length=10, choices=PaymentMethod.choices)
    expense_date = models.DateField('Дата расхода')
    comment = models.TextField('Комментарий', blank=True)
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses',
        verbose_name='Владелец',
    )

    class Meta:
        ordering = ['-expense_date', '-created_at']
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'

    def __str__(self):
        return f'{self.name} — {self.amount}'

    def clean(self):
        errors = {}

        if self.amount is not None and self.amount <= 0:
            errors['amount'] = 'Сумма должна быть больше нуля.'

        if self.expense_date and self.expense_date > timezone.localdate():
            errors['expense_date'] = 'Дата расхода не может быть в будущем.'

        name = (self.name or '').strip()
        if len(name) < 3:
            errors['name'] = 'Название должно содержать минимум 3 символа после удаления пробелов по краям.'

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.name = self.name.strip()
        super().save(*args, **kwargs)
