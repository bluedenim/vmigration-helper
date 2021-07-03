import subprocess
from typing import List, Optional

from django.core.management import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.recorder import MigrationRecorder


MIGRATE_COMMAND = 'python manage.py migrate {app} {name}'


class Command(BaseCommand):
    """
    Rolls back migrations by unapplying entries in the migration records (django_migrations) whose IDs are greater
    than the ID provided.

    **NOTE**: the process is **NOT** atomic; As soon as any of the migrations fail, the process will halt. However,
    successfully rolled-back migrations so far will remain rolled back.

    For example, to roll back all migrations *after* ID 7::

        python manage.py migration_rollback 7

    Optional parameters:

        * --dry-run
            only print the commands; don't run them
        * --migrate-cmd "command template"
            use the template provided to invoke the migrations (default is "python manage.py migrate {app} {name}")
            the placeholders "{app}" and "{name}" indicate the app name and migration file name, respectively

        For example, to see the rollback commands using pipevn (without running them):

        python manage.py migration_rollback 7 --dry-run --migrate-cmd "pipenv run python manage.py migrate {app} {name}"

    """

    @staticmethod
    def squash_migrations(migrations: List[MigrationRecorder.Migration]) -> List[MigrationRecorder.Migration]:
        """
        Find contiguous migrations for the same app and squash them by omitting all but the last entry. The incoming
        list, therefore, must be ordered such that the last entry of a contiguous group is the one to keep (e.g.
        in descending order when rolling back).

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

    @staticmethod
    def previous_migration(
        migration_recorder: MigrationRecorder,
        migration: MigrationRecorder.Migration
    ) -> Optional[MigrationRecorder.Migration]:
        """
        Retrieve the previous migration record (based on the app and ID) from the DB if one exists.

        :param migration_recorder: the MigrationRecorder instance to use to access migration records.
        :param migration: the migration to retrieve the previous migration for.

        :returns: the previous migration if one exists
        """
        return migration_recorder.migration_qs.filter(app=migration.app, id__lt=migration.id).order_by('-id').first()

    def add_arguments(self, parser):
        parser.add_argument(
            'to_id',
            type=int,
            help=(
                'The ID of the migration record to rollback to. '
                'All migrations done after this ID will be rolled back. '
                'Use "migration_records" to see all records.'
            )
        )

        parser.add_argument(
            '--dry-run',
            action='store_true',
            help=f'Show the commands that would have run but do not run them'
        )

        parser.add_argument(
            '--migrate-cmd',
            default=MIGRATE_COMMAND,
            help=f'The migration command template (accepts {{app}} and {{name}}). Default is: "{MIGRATE_COMMAND}"'
        )

    def handle(self, *args, **options):
        connection = connections[DEFAULT_DB_ALIAS]
        connection.prepare_database()
        recorder = MigrationRecorder(connection)

        rollback_to_id = options['to_id']
        dry_run = options['dry_run']
        migrate_cmd = options['migrate_cmd']

        qs = recorder.migration_qs.filter(id__gt=rollback_to_id).order_by('-id')
        migration_records = list(qs)  # type: List[MigrationRecorder.Migration]
        squashed_migrations = self.squash_migrations(migration_records)
        targets = []
        for migration in squashed_migrations:
            previous_migration = self.previous_migration(recorder, migration)
            if previous_migration:
                targets.append((migration.app, previous_migration.name))
            else:
                targets.append((migration.app, 'zero'))

        for target in targets:
            command_to_run = migrate_cmd.format(app=target[0], name=target[1])
            print(command_to_run)
            if not dry_run:
                subprocess.run(command_to_run, check=True, shell=True)
                print()
