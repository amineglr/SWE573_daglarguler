# Generated by Django 4.1.7 on 2023-05-09 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyTellerApp', '0017_remove_story_liked_profile_likedstories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='likedstories',
            field=models.ManyToManyField(to='storyTellerApp.story'),
        ),
    ]
