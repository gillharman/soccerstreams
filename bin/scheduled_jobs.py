from django_cron import CronJobBase, Schedule

class MyCronJob(CronJobBase):
    RUNS_EVERY_MINS = 1

    schedule = Schedule(run_every_mins=RUNS_EVERY_MINS)
    code = 'soccerstreams.my_cron_job' # a unique code

    def do(selfs):
        print("Hello World")
        # scanner.scan_for_games()