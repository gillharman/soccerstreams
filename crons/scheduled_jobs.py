from django_cron import CronJobBase, Schedule
from datetime import datetime, timedelta
import pytz

from .bin import (streamableGames, storeLineups, getMatches,
                  getLineups, scraper)

from logs.models import RequestLogs, RotowireRequest
from matches.models import Match
from streamablematches.models import ScannedMatch


class StreamScraper(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.stream_scraper' # a unique code

    def do(self):
        print("Scraping for games...")
        scraper.start()
        print('Scrape Complete')


class Get_Games(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.get_games'  # a unique code

    def do(self):
        print('Retrieving games...')
        getMatches.get_matches()
        print('Matching streamable games...')
        streamableGames.match_streamable_games()
        getMatches.update_match_day()
        print('Complete.')


class Get_Lineups(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.get_lineups'  # a unique code

    def do(self):
        print('Scrapping for lineups...')
        getLineups.getLineups()
        print('Scrape complete')
        print('Storing lineups')
        storeLineups.start()
        print('Complete')


class Cleanup(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.Cleanup'  # a unique code

    def do(self):
        logs_keep_history = 7  # Number of days
        matches_keep_history = 30
        # Clean up Logs
        logs_dt = datetime.today() - timedelta(days=logs_keep_history)
        logs_dt = logs_dt.replace(tzinfo=pytz.utc)
        logs = RequestLogs.objects.filter(created__lt=logs_dt)
        logs.delete()

        rotowire_logs = RotowireRequest.objects.filter(created__lt=logs_dt)
        rotowire_logs.delete()

        # Clean up matches
        matches_dt = datetime.today() - timedelta(days=matches_keep_history)
        matches_dt = matches_dt.replace(tzinfo=pytz.utc)
        matches = Match.objects.filter(created__lt=matches_dt)
        matches.delete()

        scanned_matches = ScannedMatch.objects.filter(created__lt=matches_dt)
        scanned_matches.delete()