# Generated by Django 2.2.7 on 2020-01-26 19:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0005_auto_20191128_1844'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='team',
            table='team',
        ),
        migrations.AlterModelTable(
            name='team_logo',
            table='team_logo',
        ),
        migrations.AlterModelTable(
            name='teams_in_league',
            table='teams_in_league',
        ),
    ]