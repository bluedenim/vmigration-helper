from vmigration_helper.helpers.command import MigrationCommand


class Command(MigrationCommand):
    """
    Deletes a migration record from django_migrations. This operation is a low-level operation and
    should be used only as a last resort when a migration cannot be rolled back, and deleting a record that is a
    dependency of other migrations will cause those migrations to be broken, so avoid deleting non-leaf migrations
    unless you plan to also delete other migrations that depend on the record.
    """

    def add_arguments(self, parser):
        super().add_arguments(parser)
        parser.add_argument(
            'app',
            help=(
                'The application name of the migration record to delete.'
            )
        )
        parser.add_argument(
            'name',
            help=(
                'The migration name of the migration record to delete.'
            )
        )
        parser.add_argument(
            '--yes',
            action='store_true',
            help=(
                'Runs the operation without confirmation.'
            )
        )

    def handle(self, *args, **options):
        app = options['app']
        name = options['name']
        yes = options['yes']
        if app and name:
            helper = self.create_migration_helper()

            if not yes:
                record = helper.get_migration_records_qs().filter(app=app, name=name)
                if record.exists():
                    if 'yes' == input(f'Confirm deletion of {app}:{name} (yes or no): '):
                        yes = True
                else:
                    print(f"No records found for {app}:{name}")
            if yes:
                deleted = helper.delete_migration(app, name)

                print(f"Migration record {app}:{name} deleted: {deleted}")
            else:
                print("Nothing done.")
