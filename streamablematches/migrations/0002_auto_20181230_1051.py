# Generated by Django 2.1.2 on 2018-12-30 15:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streamablematches', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='streamablematch',
            old_name='streamable_games',
            new_name='scanned_match',
        ),
    ]
