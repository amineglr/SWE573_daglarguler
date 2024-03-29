# Generated by Django 4.1.7 on 2023-05-10 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyTellerApp', '0019_alter_story_decade_alter_story_month_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='date_format',
            field=models.IntegerField(choices=[(1, 'choose a date type'), (2, 'Exact Date'), (3, 'Session'), (4, 'Decade'), (5, 'Year'), (6, 'Month'), (7, 'Date Range')]),
        ),
        migrations.AlterField(
            model_name='story',
            name='decade',
            field=models.IntegerField(blank=True, choices=[(1, 'choose a decade'), (2, "2020's"), (3, "2010's"), (4, "2000's"), (5, "1990's"), (6, "1980's"), (7, "1970's"), (8, "1960's"), (9, "1950's")], null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='month',
            field=models.IntegerField(blank=True, choices=[(1, 'choose a month'), (2, 'January'), (3, 'February'), (4, 'March'), (5, 'April'), (6, 'May'), (7, 'June'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')], null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='session',
            field=models.IntegerField(blank=True, choices=[(1, 'choose a session'), (2, 'fall'), (3, 'winter'), (4, 'spring'), (5, 'summer')], null=True),
        ),
    ]
