from typing import List, Type

from migrations.create_recipes_table import FirstMigration
from src.adaptors.database.migrations import AbstractMigration

migrations: List[Type[AbstractMigration]] = [
    FirstMigration
]
