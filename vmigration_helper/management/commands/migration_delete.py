from django.core.management import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.recorder import MigrationRecorder

from vmigration_helper.helpers.migration_records import MigrationRecordsHelper


class Command(BaseCommand):
    """
    Deletes a migration record from django_migrations. This operation is a low-level operation and
    should be used only as a last resort when a migration cannot be rolled back, and deleting a record that is a
    dependency of other migrations will cause those migrations to be broken, so avoid deleting non-leaf migrations
    unless you plan to also delete other migrations that depend on the record.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            'id',
            type=int,
            help=(
                'The ID of the migration record to delete.'
            )
        )

    def handle(self, *args, **options):
        id_to_delete = options['id']

        if id_to_delete:
            connection = connections[DEFAULT_DB_ALIAS]
            connection.prepare_database()
            helper = MigrationRecordsHelper(MigrationRecorder(connection))

            deleted = helper.delete_migration(id_to_delete)

            print(f"Migration record {id_to_delete} deleted: {deleted}")
