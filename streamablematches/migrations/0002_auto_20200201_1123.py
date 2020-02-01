# Generated by Django 2.2.7 on 2020-02-01 16:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('streamablematches', '0001_squashed_0006_auto_20200128_2115'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LeagueCopy',
            new_name='League',
        ),
        migrations.RenameModel(
            old_name='LineupCopy',
            new_name='Lineup',
        ),
        migrations.RenameModel(
            old_name='MatchCopy',
            new_name='Match',
        ),
        migrations.RenameModel(
            old_name='TeamCopy',
            new_name='Team',
        ),
        migrations.RenameModel(
            old_name='TeamsInLeagueCopy',
            new_name='TeamInLeague',
        ),
        migrations.RenameModel(
            old_name='TeamLogoCopy',
            new_name='TeamLogo',
        ),
        migrations.AlterModelOptions(
            name='league',
            options={'verbose_name': 'league', 'verbose_name_plural': 'leagues'},
        ),
        migrations.AlterModelOptions(
            name='lineup',
            options={'verbose_name': 'lineup', 'verbose_name_plural': 'lineups'},
        ),
        migrations.AlterModelOptions(
            name='link',
            options={'verbose_name': 'link', 'verbose_name_plural': 'links'},
        ),
        migrations.AlterModelOptions(
            name='match',
            options={'verbose_name': 'match', 'verbose_name_plural': 'matches'},
        ),
        migrations.AlterModelOptions(
            name='scannedmatch',
            options={'verbose_name': 'scanned match', 'verbose_name_plural': 'scanned matches'},
        ),
        migrations.AlterModelOptions(
            name='streamablematch',
            options={'verbose_name': 'streamable match', 'verbose_name_plural': 'streamable matches'},
        ),
        migrations.AlterModelOptions(
            name='team',
            options={'verbose_name': 'teams'},
        ),
        migrations.AlterModelOptions(
            name='teaminleague',
            options={'verbose_name': 'team in league', 'verbose_name_plural': 'team in leagues'},
        ),
        migrations.AlterModelOptions(
            name='teamlogo',
            options={'verbose_name': 'team logo', 'verbose_name_plural': 'team logos'},
        ),
        migrations.AlterModelTable(
            name='league',
            table='competitions_league',
        ),
        migrations.AlterModelTable(
            name='lineup',
            table='competitions_lineup',
        ),
        migrations.AlterModelTable(
            name='link',
            table='streamablematches_link',
        ),
        migrations.AlterModelTable(
            name='match',
            table='competitions_match',
        ),
        migrations.AlterModelTable(
            name='scannedmatch',
            table='streamablematches_scanned_match',
        ),
        migrations.AlterModelTable(
            name='streamablematch',
            table='streamablematches_streamable_match',
        ),
        migrations.AlterModelTable(
            name='team',
            table='competitions_team',
        ),
        migrations.AlterModelTable(
            name='teaminleague',
            table='competitions_team_in_league',
        ),
        migrations.AlterModelTable(
            name='teamlogo',
            table='competitions_team_logo',
        ),
    ]
