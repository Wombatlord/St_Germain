import sys
from typing import Dict, Callable, Any

from migrations.migrationsRegistry import migrations
from src.adaptors.database.commands import run, flush

if __name__ == "__main__":
    options: Dict[str, Callable[[Any], None]] = {
        "migrate": run,
        "flush": flush
    }

    if __name__ == "__main__":
        def error(arg):
            optionsString = ', '.join(list(options.keys()))
            print(f"The command '{arg}' does not exist, available commands are {optionsString}")


        args = sys.argv
        command = options.get(args[1], error)
        command(migrations)
