# Generated by Django 4.1 on 2022-08-31 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_customuser_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='registration_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
