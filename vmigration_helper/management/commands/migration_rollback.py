import subprocess
from typing import List

from django.core.management import BaseCommand
from django.db import DEFAULT_DB_ALIAS, connections, OperationalError
from django.db.migrations.recorder import MigrationRecorder

from vmigration_helper.helpers.migration_records import MigrationRecordsHelper

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
        rollback_to_id = options['to_id']
        dry_run = options['dry_run']
        migrate_cmd = options['migrate_cmd']

        try:
            connection = connections[DEFAULT_DB_ALIAS]
            connection.prepare_database()
            helper = MigrationRecordsHelper(MigrationRecorder(connection))
            qs = helper.get_migration_records_qs().filter(id__gt=rollback_to_id).order_by('-id')
            migration_records = list(qs)  # type: List[MigrationRecorder.Migration]
            squashed_migrations = helper.squash_migrations(migration_records)
            targets = []
            for migration in squashed_migrations:
                previous_migration = helper.previous_migration(migration)
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
        except OperationalError as e:
            print(f'DB ERROR: {e}')
            exit(1)
