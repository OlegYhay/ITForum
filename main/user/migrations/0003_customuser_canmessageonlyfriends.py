# Generated by Django 4.1 on 2022-09-08 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_friendrequest_status_alter_friends_user_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='CanMessageOnlyFriends',
            field=models.BooleanField(default=False, verbose_name='Сообщения могут писать только друзья'),
        ),
    ]
