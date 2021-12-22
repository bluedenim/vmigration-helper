from typing import List, Optional

from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.recorder import MigrationRecorder
from django.db.models import QuerySet


class MigrationRecordsHelper:
    """
    Helper for migration records
    """

    def __init__(self, migration_recorder: Optional[MigrationRecorder] = None) -> None:
        if not migration_recorder:
            connection = connections[DEFAULT_DB_ALIAS]
            connection.prepare_database()

            migration_recorder = MigrationRecorder(connection)
        self.migration_recorder = migration_recorder

    def get_migration_records_qs(self) -> QuerySet:
        """
        Gets a QuerySet from which MigrationRecorder.Migration records can be acquired.

        Args:
            migration_recorder - instance of MigrationRecorder used to get migration records
        Returns:
            query set to use to get migration records
        """
        return self.migration_recorder.migration_qs

    def previous_migration(self, migration: MigrationRecorder.Migration) -> Optional[MigrationRecorder.Migration]:
        """
        Retrieve the previous migration record (based on the app and ID) from the DB if one exists.

        :param migration_recorder: the MigrationRecorder instance to use to access migration records.
        :param migration: the migration to retrieve the previous migration for.

        :returns: the previous migration if one exists
        """
        return self.migration_recorder.migration_qs.filter(
            app=migration.app, id__lt=migration.id
        ).order_by('-id').first()

    def delete_migration(self, app: str, name: str) -> bool:
        """
        Delete the migration matching the app and name given.

        :returns: True if a record was deleted
        """
        deleted, _ = self.migration_recorder.migration_qs.filter(app=app, name=name).delete()
        return deleted

    @staticmethod
    def squash_migrations(migrations: List[MigrationRecorder.Migration]) -> List[MigrationRecorder.Migration]:
        """
        Find contiguous migrations for the same app and squash them by omitting all but the last entry. The incoming
        list, therefore, must be ordered such that the last entry of a contiguous group is the one to keep (e.g.
        in descending order when rolling back).

        For example:
          input: app 1, migration 5
                 app 1, migration 4
                 app 1, migration 3
                 app 2, migration 11
                 app 2, migration 10

          output: app 1, migration 3
                  app 2, migration 10

        :param migrations: the migrations to squash

        :returns: the squashed migrations
        """
        lowest_migrations = []  # type: List[MigrationRecorder.Migration]
        curr_app = None
        curr_migration = None
        for migration in migrations:
            if curr_app is None:
                curr_app = migration.app
                curr_migration = migration
            else:
                if curr_app == migration.app:
                    curr_migration = migration
                else:
                    lowest_migrations.append(curr_migration)
                    curr_app = migration.app
                    curr_migration = migration
        if curr_migration:
            lowest_migrations.append(curr_migration)
        return lowest_migrations
