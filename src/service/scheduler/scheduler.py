from apscheduler.schedulers.background import BackgroundScheduler
import sys
from logging import getLogger

logger = getLogger(__name__)

def setup_scheduler_for_payments():
    scheduler = BackgroundScheduler()
    scheduler.add_job(check_for_payments_statuses, 'interval', minutes=1)
    scheduler.start()


def check_for_payments_statuses():
    print('Scheduler scheduling', file=sys.stderr)