from django.db import OperationalError
from django.db.models import Max

from vmigration_helper.helpers.command import MigrationCommand


class Command(MigrationCommand):
    """
    Displays the ID of the last entry in the migration records (from the ``django_migrations`` table).
    """

    def create_snapshot_name(self) -> int:
        """
        Returns the current max ID of the migration records table (django_migrations). If there are no records,
        0 is returned.
        """
        helper = self.create_migration_helper()
        latest_migration_id = helper.get_migration_records_qs().aggregate(Max('id'))['id__max']
        return latest_migration_id or 0

    def handle(self, *args, **options):
        try:
            print(self.create_snapshot_name())
        except OperationalError as e:
            print(f'DB ERROR: {e}')
            exit(1)
