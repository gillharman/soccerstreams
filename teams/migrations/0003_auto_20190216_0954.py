# Generated by Django 2.1.2 on 2019-02-16 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0002_team_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team_logo',
            name='logo',
            field=models.ImageField(upload_to='team_logos'),
        ),
    ]
