from src.adaptors.database.migrations import MigrationRunner


def run(migrations):
    for migration in migrations:
        MigrationRunner.registerMigration(migration)
    MigrationRunner.runAll()


def flush(migrations):
    MigrationRunner.init_db()
    run(migrations)
