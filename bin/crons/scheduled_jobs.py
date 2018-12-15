from django_cron import CronJobBase, Schedule

from bin.scanner import scanner


class StreamScraper(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.stream_scraper' # a unique code

    def do(selfs):
        print("Scraping...")
        scanner.start_scraper()
        print('Scrape Complete')

class Get_Games(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.get_games'  # a unique code