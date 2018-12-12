# Generated by Django 2.1.2 on 2018-12-12 02:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('leagues', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('short_name', models.CharField(max_length=30)),
                ('venue', models.CharField(max_length=30)),
                ('club_colors', models.CharField(max_length=30)),
                ('crest', models.CharField(max_length=2083)),
                ('league', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='leagues.League')),
            ],
        ),
    ]
