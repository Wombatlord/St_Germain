from __future__ import annotations

import sys
from typing import List, Type, Tuple, Dict, Callable

from src.adaptors.database.db_adaptor import get_cursor, commit
from migrations.create_recipes_table import FirstMigration


# Noob Note:
#
# A "Migration" is something which makes a change to database SCHEMA.
# It should be an incremental change which is reversible.
# The history of migrations is representative of versions of the DB structure.
# The Schema defines the structure of the database.
# eg. Adding / removing tables, adding / removing columns to / from tables.


class RegisteredMigrations:
    migrations: List[Type[AbstractMigration]] = [
        FirstMigration,
    ]


class AbstractMigration:
    """
    Generic Migration.
    Further specific migrations should inherit and implement these methods.
    """
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
    """
    MigrationRunner handles running a migration sequence.
    """
    migrations: List[Tuple[str, Type[AbstractMigration]]] = {}

    @classmethod
    def registerMigration(cls, migration: Type[AbstractMigration]) -> None:
        """
        Checks whether a migration is already registered to be run.
        If the migration is currently unregistered (i.e. new), it will
        be added to the migrations list.
        """
        migrationExists = any(
            migration.getMigrationID() == existingMigrationID for existingMigrationID, migration in cls.migrations)
        if not migrationExists:
            cls.migrations.append((migration.getMigrationID(), migration))

    @classmethod
    def runMigrations(cls, migration: Type[AbstractMigration]) -> None:
        """
        Checks the migration list for registered migrations
        and runs them in sequence.
        """
        sql = f"SELECT id FROM migrations WHERE id = '{migration.getMigrationID()}'"
        migrationExists = get_cursor().execute(sql).fetchOne()
        if not migrationExists:
            migration.run()


    @classmethod
    def init_db(cls) -> None:

        sql = """
            DROP SCHEMA public CASCADE;
            CREATE SCHEMA public; 
            create table migrations
            (
                id varchar(255)           
            );

            create unique index migrations_sequence_uindex
                on migrations (id);

            alter table migrations
                add constraint migrations_id
            primary key (id);    
        """

        get_cursor().execute(sql)


def run():
    for migration in RegisteredMigrations.migrations:
        MigrationRunner.registerMigration(migration)
    MigrationRunner.runMigrations()


def flush():
    MigrationRunner.init_db()
    run()


options: Dict[str: Callable[[str], None]] = {
    "run": run,
    "flush": flush
}


if __name__ == "__main__":
    def error(arg):
        optionsString = ', '.join(list(options.keys()))
        print(f"The command '{arg}' does not exist, available commands are {optionsString}")
    args = sys.argv
    command = options.get(args[1], error)
    command()
