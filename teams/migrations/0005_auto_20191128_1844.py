# Generated by Django 2.2.7 on 2019-11-28 23:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0004_auto_20191128_1821'),
    ]

    operations = [
        migrations.RenameField(
            model_name='team',
            old_name='league',
            new_name='leagues',
        ),
    ]
