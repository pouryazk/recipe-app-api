import time

from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand
# Django management commands are included in the docs (folder)


class Command(BaseCommand):
    """ django command to pause execution until database is available """

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                 self.stdout.write('Database unavailable, waiting one second')
                 time.sleep(1)

        self.stdout.write(self.style.SUCCESS('DATABASE available!'))
        # the style is for showing string as green meaning to be successful.
        
