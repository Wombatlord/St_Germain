from __future__ import annotations

from typing import List, Type, Tuple

from src.adaptors.database.db_adaptor import get_cursor, commit


class AbstractMigration:
    """
    Generic Migration.
    Further specific migrations should inherit and implement these methods.

    A "Migration" is something which makes a change to database SCHEMA.
    It should be an incremental change which is reversible.
    The history of migrations is representative of versions of the DB structure.
    The Schema defines the structure of the database.
    eg. Adding / removing tables, adding / removing columns to / from tables.
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
    migrations: List[Tuple[str, Type[AbstractMigration]]] = []

    @classmethod
    def registerMigration(cls, migration: Type[AbstractMigration]) -> None:
        """
        Checks whether a migration is already registered to be run.
        If the migration is currently unregistered (i.e. new), it will
        be added to the migrations list.
        """
        migrationExists = any(
            migration.getMigrationID() == existingMigrationID for existingMigrationID, migration in cls.migrations
        )
        if not migrationExists:
            cls.migrations.append((migration.getMigrationID(), migration))

    @classmethod
    def runMigration(cls, migration: Type[AbstractMigration]) -> None:
        """
        Checks the migration list for registered migrations
        and runs them in sequence.
        """
        sql = f"SELECT id FROM migrations WHERE id = '{migration.getMigrationID()}'"
        migrationExists = get_cursor().execute(sql)
        if not migrationExists:
            migration.run()

    @classmethod
    def runAll(cls) -> None:
        for identifier, migration in cls.migrations:
            cls.runMigration(migration)
            print(f"Ran migration: {identifier}")

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
