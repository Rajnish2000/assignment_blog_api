
from django.db.utils import OperationalError
from psycopg2 import OperationalError as psycopg2OpError
from django.core.management.base import BaseCommand
import time


class Command(BaseCommand):
    """Django command to pause execution until database is available."""

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))
