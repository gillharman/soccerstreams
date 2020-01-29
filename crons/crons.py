from django_cron import CronJobBase, Schedule
from datetime import datetime, timedelta
import pytz

from crons.scripts import getmatches, scraper, storelineups, getlineups, streamablegames

from streamablematches.models.competitions import MatchCopy
from streamablematches.models.logs import RequestLog, RotowireRequestLog
from streamablematches.models.streamablematches import ScannedMatch


class StreamScraper(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.stream_scraper' # a unique code

    def do(self):
        print("Scraping for games...")
        scraper.start()
        print('Scrape Complete')


class GetGames(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.get_games'  # a unique code

    def do(self):
        print('Retrieving games...')
        getmatches.get_matches()
        print('Matching streamable games...')
        streamablegames.match_streamable_games()
        print("Updating current match day...")
        getmatches.update_match_day()
        print('Complete')


class GetLineups(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.get_lineups'  # a unique code

    def do(self):
        print('Scrapping for lineups...')
        getlineups.get_lineups()
        print('Scrape complete')
        print('Storing lineups')
        storelineups.start()
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
        logs = RequestLog.objects.filter(created__lt=logs_dt)
        logs.delete()

        rotowire_logs = RotowireRequestLog.objects.filter(created__lt=logs_dt)
        rotowire_logs.delete()

        # Clean up matches
        matches_dt = datetime.today() - timedelta(days=matches_keep_history)
        matches_dt = matches_dt.replace(tzinfo=pytz.utc)
        matches = MatchCopy.objects.filter(created__lt=matches_dt)
        matches.delete()

        scanned_matches = ScannedMatch.objects.filter(created__lt=matches_dt)
        scanned_matches.delete()