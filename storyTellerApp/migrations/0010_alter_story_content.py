# Generated by Django 4.1.7 on 2023-05-05 21:40

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storyTellerApp', '0009_alter_story_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]