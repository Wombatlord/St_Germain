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
                recipe_id serial, 
                author varchar(255),
                title varchar(255),
                cook_time varchar(255),
                method text,
                serves varchar(255),
                primary key(recipe_id)
            ); 
        """

        cls.migrations.append(sql)

    @classmethod
    def _createIngredientsTable(cls) -> None:
        sql = """
            create table ingredients
            (   
                ingredients_id serial,
                recipe_id INT,
                ingredient text not null,
                quantity varchar(255) not null
            );
            
            create unique index ingredients_sequence_uindex
                on ingredients (ingredients_id);
        """

        cls.migrations.append(sql)

    @classmethod
    def _createMethodTable(cls) -> None:
        sql = """
                create table method
                (   
                    method_id serial,
                    recipe_id INT,
                    method text not null                  
                );

                create unique index method_sequence_uindex
                    on method (method_id);
            """

        cls.migrations.append(sql)

    @classmethod
    def addSQL(cls) -> None:
        cls._createRecipesTable()
        cls._createIngredientsTable()
        cls._createMethodTable()
