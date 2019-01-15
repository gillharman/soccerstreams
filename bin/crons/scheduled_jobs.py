from django_cron import CronJobBase, Schedule

from bin.crons.bin import streamableGames, getMatches, storeMatches, scraper


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
        data = getMatches.get_matches()
        storeMatches.store_matches(data)
        print('Matching streamable games...')
        streamableGames.match_streamable_games()
        print('Complete.')

class Get_Linueups(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.get_lineups'  # a unique code

    def do(self):
        print('Hello World')