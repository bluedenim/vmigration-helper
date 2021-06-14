from django.core.management import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.recorder import MigrationRecorder


class Command(BaseCommand):
    """
    Displays all the migration records (from the ``django_migrations`` table).
    """

    def handle(self, *args, **options):
        connection = connections[DEFAULT_DB_ALIAS]
        connection.prepare_database()
        recorder = MigrationRecorder(connection)

        print("ID,Applied,App,Name")
        for record in recorder.migration_qs.all():
            print(f"{record.id},{record.applied.isoformat()},{record.app},{record.name}")
