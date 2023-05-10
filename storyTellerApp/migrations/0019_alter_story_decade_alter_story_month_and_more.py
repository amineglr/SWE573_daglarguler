# Generated by Django 4.1.7 on 2023-05-10 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storyTellerApp', '0018_alter_profile_likedstories'),
    ]

    operations = [
        migrations.AlterField(
            model_name='story',
            name='decade',
            field=models.IntegerField(choices=[(1, "2020's"), (2, "2010's"), (3, "2000's"), (4, "1990's"), (5, "1980's"), (6, "1970's"), (7, "1960's"), (8, "1950's")], null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='month',
            field=models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'August'), (8, 'September'), (9, 'October'), (10, 'November'), (11, 'December')], null=True),
        ),
        migrations.AlterField(
            model_name='story',
            name='session',
            field=models.IntegerField(choices=[(1, 'fall'), (2, 'winter'), (3, 'spring'), (4, 'summer')], null=True),
        ),
    ]
