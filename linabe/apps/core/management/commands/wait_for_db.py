import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
from os import environ

class Command(BaseCommand):
    # Command to pause execution until database is available

    def handle(self, *args, **options):
        # Handle the command
        self.stdout.write('Waiting for linaee database.')
        time_out = int(environ.get('DB_WAIT_TIME_OUT','45'))
        time_out_count = 0
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, waiting 1 second...')
                time_out_count += 1
                if (time_out_count >= time_out):
                    break
                time.sleep(1)

        if time_out_count == 0:
            time.sleep(int(environ.get('DB_WAIT_TIME_EXTRA','45')))

        self.stdout.write(self.style.SUCCESS('Database available! (' + str(time_out_count) + 'sec)' ))