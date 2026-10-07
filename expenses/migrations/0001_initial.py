from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=120, verbose_name='Название')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма')),
                ('category', models.CharField(choices=[('food', 'Продукты'), ('transport', 'Транспорт'), ('education', 'Обучение'), ('entertainment', 'Развлечения'), ('health', 'Здоровье'), ('other', 'Другое')], max_length=20, verbose_name='Категория')),
                ('payment_method', models.CharField(choices=[('cash', 'Наличные'), ('card', 'Карта')], max_length=10, verbose_name='Способ оплаты')),
                ('expense_date', models.DateField(verbose_name='Дата расхода')),
                ('comment', models.TextField(blank=True, verbose_name='Комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenses', to=settings.AUTH_USER_MODEL, verbose_name='Владелец')),
            ],
            options={
                'verbose_name': 'Расход',
                'verbose_name_plural': 'Расходы',
                'ordering': ['-expense_date', '-created_at'],
            },
        ),
    ]
