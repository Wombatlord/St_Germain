# St_Germain

A python project for learning about working with an API.
Implemented in python with discord.py.

Uses https://rws-cards-api.herokuapp.com/ for tarot data.

## Database Management

The database management CLI for St Germaine is known as golem. Golem can be invoked in the following ways:


### Flush
To drop and replace the database schema:
```shell
python golem.py flush
```
__WARNING__: This will purge any data currently in the database!

### Run Migrations
To run pending migrations:
```shell
python golem.py migrate
```

