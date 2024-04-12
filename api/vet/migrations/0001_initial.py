# Generated by Django 4.2.6 on 2024-04-09 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Имя')),
                ('surname', models.CharField(max_length=150, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=15, verbose_name='Телефон')),
                ('telegram_id', models.CharField(max_length=300, unique=True)),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(verbose_name='Дата записи')),
                ('pet', models.CharField(max_length=200, verbose_name='Вид животного')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='vet.client', verbose_name='Хозяин')),
            ],
        ),
    ]
