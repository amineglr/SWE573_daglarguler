# Generated by Django 4.1.7 on 2023-05-15 14:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storyTellerApp', '0024_alter_comment_story'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='post_id',
        ),
    ]