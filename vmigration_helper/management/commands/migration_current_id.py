from django.core.management import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.recorder import MigrationRecorder
from django.db.models import Max


class Command(BaseCommand):
    """
    Displays the ID of the last entry in the migration records (from the ``django_migrations`` table).
    """

    @staticmethod
    def create_snapshot_name(connection):
        migration_recorder = MigrationRecorder(connection)
        latest_migration_id = migration_recorder.migration_qs.aggregate(Max('id'))['id__max']
        return str(latest_migration_id)

    def handle(self, *args, **options):
        connection = connections[DEFAULT_DB_ALIAS]
        connection.prepare_database()

        print(self.create_snapshot_name(connection))
