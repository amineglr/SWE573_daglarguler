# Generated by Django 4.1.7 on 2023-05-24 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyTellerApp', '0027_alter_story_date_exact_alter_story_date_exact_end'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='date_format',
            field=models.CharField(blank=True, choices=[(1, 'choose a date type'), (2, 'Exact Date'), (3, 'Date Range')], max_length=100, null=True),
        ),
    ]
