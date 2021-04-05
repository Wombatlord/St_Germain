from typing import List, Type, Tuple

from src.adaptors.database.db_adaptor import get_cursor, commit
from migrations.init_db import FirstMigration


class AbstractMigration:
    migrations: List[str] = []
    cursor = get_cursor()

    @classmethod
    def run(cls) -> None:
        cls.addSQL()
        cls.migrations.append(
            f"INSERT INTO migrations (id) VALUES ('{cls.getMigrationID()}')"
        )
        for sql in cls.migrations:
            cls.cursor.execute(sql)

        commit()

    @classmethod
    def getMigrationID(cls) -> str:
        pass

    @classmethod
    def addSQL(cls) -> None:
        pass


class MigrationRunner:
    migrations: List[Tuple[str, Type[AbstractMigration]]] = {}

    @classmethod
    def registerMigration(cls, migration: Type[AbstractMigration]) -> None:
        migrationExists = any(
            migration.getMigrationID() == existingMigrationID for existingMigrationID, migration in cls.migrations)
        if not migrationExists:
            cls.migrations.append((migration.getMigrationID(), migration))

    @classmethod
    def runMigrations(cls) -> None:
        for migrationID, migration in cls.migrations:
            migrationExists = get_cursor().execute(f"SELECT id FROM migrations WHERE id = '{migrationID}'").fetchOne()
            if not migrationExists:
                migration.run()


def run():
    MigrationRunner.registerMigration(FirstMigration)
    MigrationRunner.runMigrations()
