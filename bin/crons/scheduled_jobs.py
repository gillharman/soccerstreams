from django_cron import CronJobBase, Schedule

from bin.scanner import scanner


class MyCronJob(CronJobBase):
    RUNS_EVERY_MINS = 0

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.my_cron_job' # a unique code

    def do(selfs):
        print("Scraping...")
        scanner.start_scraper()
        print('Scrape Complete')