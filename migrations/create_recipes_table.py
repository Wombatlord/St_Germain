from typing import List

from src.adaptors.database.migrations import AbstractMigration


class FirstMigration(AbstractMigration):
    migrations: List[str] = []

    @classmethod
    def getMigrationID(cls) -> str:
        return "create_recipes_table"

    @classmethod
    def _createRecipesTable(cls) -> None:
        sql = """
            create table recipes
            (
                id serial, 
                author varchar(255) not null,
                title varchar(255) not null,
                ingredients text not null,
                cook_time varchar(255) not null,
                method text not null,
                serves varchar(255) not null            
            );

            create unique index recipes_sequence_uindex
                on recipes (id);    
        """

        cls.migrations.append(sql)

    @classmethod
    def addSQL(cls) -> None:
        cls._createRecipesTable()


