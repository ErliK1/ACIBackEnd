'''
Handle wait for db postgres to be available.

'''
from django.core.management import BaseCommand

from psycopg2 import OperationalError as PsyCop2gError

from django.db.utils import OperationalError


class Command(BaseCommand):

    def handle(self, *args, **options):
        pass
