from abc import ABC

from django.core.management import BaseCommand
from django.db import connections, DEFAULT_DB_ALIAS
from django.db.migrations.recorder import MigrationRecorder

from vmigration_helper.helpers.migration_records import MigrationRecordsHelper


class MigrationCommand(BaseCommand, ABC):
    """
    Abstract base class for migration commands in this app.

    This class provides a place for common concerns to all migration commands to be implemented. For instance, it
    registers the "connection-name" optional parameter to the command and surfaces the parameter as
    the "connection_name" property.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            '--connection-name',
            default=DEFAULT_DB_ALIAS,
            help=f'The connection to use for migration commands. Defaults to settings.DEFAULT_DB_ALIAS'
        )

    def execute(self, *args, **options):
        self.connection_name = options["connection_name"]
        super().execute(*args, **options)

    def create_migration_helper(self, connection=None) -> MigrationRecordsHelper:
        """
        Initializes a connection and returns an instance of MigrationRecordsHelper initialized to the connection
        provided.

        :param connection: optional connection to use. If not provided, a connection to the current connection name
            is created and used. If a connection is provided, its prepare_database() MUST have been called.

        :returns: an instance of MigrationRecordsHelper
        """
        if not connection:
            connection = connections[self.connection_name]
            connection.prepare_database()
        return MigrationRecordsHelper(MigrationRecorder(connection))

    @property
    def connection_name(self) -> str:
        return self._connection_name

    @connection_name.setter
    def connection_name(self, value: str) -> None:
        self._connection_name = value
