# Generated by Django 2.1.2 on 2018-12-14 02:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0003_team_api_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='tla',
            field=models.CharField(default='Null', max_length=10),
            preserve_default=False,
        ),
    ]
