# Generated by Django 2.1.2 on 2018-12-13 02:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='code',
            field=models.CharField(default='null', max_length=10),
            preserve_default=False,
        ),
    ]
