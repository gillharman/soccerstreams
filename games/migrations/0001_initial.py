# Generated by Django 2.1.2 on 2018-11-09 16:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('match', models.CharField(max_length=100)),
                ('postUrl', models.CharField(default='https://reddit.com/soccerstreams', max_length=2083)),
                ('time', models.CharField(max_length=14)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('streamer', models.CharField(default=None, max_length=100)),
                ('link', models.CharField(default=None, max_length=100)),
                ('linkScore', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('match', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='games.Game')),
            ],
        ),
        migrations.CreateModel(
            name='Logs',
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
