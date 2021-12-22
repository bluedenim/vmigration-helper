from django.core.management import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections, OperationalError
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

    def handle(self, *args, **options):
        try:
            connection = connections[DEFAULT_DB_ALIAS]
            connection.prepare_database()
            print(self.create_snapshot_name(connection))
        except OperationalError as e:
            print(f'DB ERROR: {e}')
            exit(1)
