# Generated by Django 4.2.4 on 2023-08-22 04:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PasswordHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(max_length=50)),
                ('created_at', models.DateField(default=datetime.date(2023, 8, 22))),
            ],
        ),
    ]
