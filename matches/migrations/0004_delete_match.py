# Generated by Django 2.2.7 on 2020-01-29 02:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lineups', '0002_delete_lineup'),
        ('streamablematches', '0006_auto_20200128_2115'),
        ('matches', '0003_auto_20200126_1435'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Match',
        ),
    ]
