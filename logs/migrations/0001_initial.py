# Generated by Django 2.1.2 on 2018-12-29 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RequestLogs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('httpStatusCode', models.CharField(max_length=10)),
                ('requestContent', models.TextField(default=None)),
                ('responseContent', models.TextField(default=None)),
                ('endPoint', models.CharField(max_length=2083)),
                ('exception', models.CharField(max_length=253)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]