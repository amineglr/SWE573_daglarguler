# Generated by Django 4.1.7 on 2023-05-07 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyTellerApp', '0014_remove_like_story_remove_like_user_like_story_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='story',
            name='no_of_likes',
            field=models.IntegerField(default=0),
        ),
    ]
