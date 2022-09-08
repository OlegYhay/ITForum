# Generated by Django 4.1 on 2022-09-01 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forumBase', '0002_forum_alter_category_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commentdislikes',
            name='CommentDislike',
        ),
        migrations.RemoveField(
            model_name='commentlikes',
            name='CommentLike',
        ),
        migrations.AlterField(
            model_name='commenttopic',
            name='CommentDislike',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='commenttopic',
            name='CommentLike',
            field=models.IntegerField(default=0),
        ),
    ]
