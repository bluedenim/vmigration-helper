from django.core.management import BaseCommand
from django.conf import settings
from django.db import connections, OperationalError
from django.db.migrations.recorder import MigrationRecorder
from django.db.models import Max

from vmigration_helper.helpers.migration_records import MigrationRecordsHelper


class Command(BaseCommand):
    """
    Displays the ID of the last entry in the migration records (from the ``django_migrations`` table).
    """

    @staticmethod
    def create_snapshot_name(connection) -> int:
        """
        Returns the current max ID of the migration records table (django_migrations). If there are no records,
        0 is returned.
        """
        helper = MigrationRecordsHelper(MigrationRecorder(connection))
        latest_migration_id = helper.get_migration_records_qs().aggregate(Max('id'))['id__max']
        return latest_migration_id or 0

    def add_arguments(self, parser):
        parser.add_argument(
            "--connection-name",
            type=str,
            default=settings.DEFAULT_DB_ALIAS,
            help=("The connection name to use. If not provided, the default connection will be used."),
        )

    def handle(self, *args, **options):
        connection_name = options["connection_name"]

        try:
            connection = connections[connection_name]
            connection.prepare_database()
            print(self.create_snapshot_name(connection))
        except OperationalError as e:
            print(f'DB ERROR: {e}')
            exit(1)
