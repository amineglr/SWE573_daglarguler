# Generated by Django 4.1.7 on 2023-05-05 12:13

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('storyTellerApp', '0006_remove_story_location_story_locations'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
    ]