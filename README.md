# Van's Migration Helper

Django commands to help with running Django migrations.

## Installation

* Add the dependency to your environment:

  ```
  pip install vmigration-helper
  ```

* Add the app `vmgration_helper.apps.VMigrationHelperConfig` to your list of installed apps in your settings:

  ```
  INSTALLED_APPS = [
    ...
    'vmigration_helper.apps.VMigrationHelperConfig',
    ...
  ]
  ```


## Commands

### migration_records

Shows existing migration records in your `django_migration` table.

#### Optional parameters:

  * `--format (console | csv)` print the info in CSV or friendlier console format (default)

```
> python manage.py migration_records --format csv
ID,Applied,App,Name
175,2021-06-13T20:41:28.683900+00:00,contenttypes,0001_initial
176,2021-06-13T20:41:28.717886+00:00,auth,0001_initial
177,2021-06-13T20:41:28.742930+00:00,admin,0001_initial
178,2021-06-13T20:41:28.761938+00:00,admin,0002_logentry_remove_auto_add
179,2021-06-13T20:41:28.770319+00:00,admin,0003_logentry_add_action_flag_choices
180,2021-06-13T20:41:28.791287+00:00,contenttypes,0002_remove_content_type_name
...
192,2021-06-13T20:41:28.991814+00:00,sessions,0001_initial
```

These are the records of migrations applied. The fields indicate:
  * ID - the ID of the record
  * Applied - when the migration was applied 
  * App - name of the Django app
  * Name - name of the migration 


### migration_current_id

Shows the ID of the latest migration record in your `django_migration` table.

```
> python manage.py migration_current_id
192
```

192 is the ID of the latest record as shown above.

### migration_rollback

Roll-back (unapply) previously applied migrations _after_ (but not including) the migration ID provided.

```
> python manage.py migration_rollback 176
```

The above will rollback migrations after `0001_initial` of the `auth` app:

```
python manage.py migrate sessions zero
Operations to perform:
  Unapply all migrations: sessions
Running migrations:
  Rendering model states... DONE
  Unapplying sessions.0001_initial... OK

python manage.py migrate auth 0001_initial
Operations to perform:
  Target specific migration: 0001_initial, from auth
Running migrations:
  Rendering model states... DONE
  Unapplying auth.0012_alter_user_first_name_max_length... OK
  Unapplying auth.0011_update_proxy_permissions... OK
  Unapplying auth.0010_alter_group_name_max_length... OK
  Unapplying auth.0009_alter_user_last_name_max_length... OK
  Unapplying auth.0008_alter_user_username_max_length... OK
  Unapplying auth.0007_alter_validators_add_error_messages... OK
  Unapplying auth.0006_require_contenttypes_0002... OK
  Unapplying auth.0005_alter_user_last_login_null... OK
  Unapplying auth.0004_alter_user_username_opts... OK
  Unapplying auth.0003_alter_user_email_max_length... OK
  Unapplying auth.0002_alter_permission_name_max_length... OK

python manage.py migrate contenttypes 0001_initial
Operations to perform:
  Target specific migration: 0001_initial, from contenttypes
Running migrations:
  Rendering model states... DONE
  Unapplying contenttypes.0002_remove_content_type_name... OK

python manage.py migrate admin zero
Operations to perform:
  Unapply all migrations: admin
Running migrations:
  Rendering model states... DONE
  Unapplying admin.0003_logentry_add_action_flag_choices... OK
  Unapplying admin.0002_logentry_remove_auto_add... OK
  Unapplying admin.0001_initial... OK
```

#### Optional parameters:

  * `--dry-run` will print the commands but will not actually run them
  * `--migrate-cmd <command to run migrations>` sets the command to run migrations with. The command must accept 
    the app and migration name as the `{app}` and `{name}` placeholders, respectively.  
    
    For example:
    
    ```
    --migrate-cmd "pipenv run python manage.py migrate {app} {name}" 
    ```
    
    can be used to have the command run migrations using `pipenv`.

    For example:

    ```
    > pipenv run python manage.py migration_rollback 0 --dry-run --migrate-cmd "pipenv run python manage.py migrate {app} {name}"
    pipenv run python manage.py migrate sessions zero
    pipenv run python manage.py migrate auth 0001_initial
    pipenv run python manage.py migrate contenttypes 0001_initial
    pipenv run python manage.py migrate admin zero
    pipenv run python manage.py migrate auth zero
    pipenv run python manage.py migrate contenttypes zero
    ```

### migration_delete

Deletes an entry from Django's migration records. This command should be
used only as a last resort to fix up migration records that cannot be rolled back. No migration up/down is performed; 
the record is simply removed from `django_migrations`.

NOTE also that migrations that depend on the record being deleted will be "broken" after the deletion, so this 
command should only be run on "leaf" migration records unless you plan to also delete other migration records that
depend on the one being deleted.

```
python manage.py migration_delete myapp 0003_some_migration
Confirm deletion of auth:0009_alter_user_last_name_max_length (yes or no): yes
```
The command above deletes the migration `0003_some_migration` for the app `myapp` (after
getting confirmation).

To delete without confirmation, use the `--yes` option:
```
python manage.py migration_delete myapp 0003_some_migration --yes
```


#### Optional parameters:

  * `--yes` will proceed to deleting the record without asking for confirmation


## Ideas for automation

Here's an idea for automating the deployment of your Django app using these utilities:

* Deploy new code
* Run `migration_current_id` and capture the current ID
* Run migration normally
* Run your automated tests normally
  * If tests pass, you're done!
  * If tests fail, and you need to rollback, run
  `migration_rollback <captured ID>`
  