from abc import ABC

from django.core.management import BaseCommand
from django.db import DEFAULT_DB_ALIAS


class MigrationCommand(BaseCommand, ABC):

    def add_arguments(self, parser):
        parser.add_argument(
            '--connection-name',
            default=DEFAULT_DB_ALIAS,
            help=f'The connection to use for migration commands. Defaults to settings.DEFAULT_DB_ALIAS'
        )
