import psycopg2

_con = None


def get_cursor():
    global _con
    if _con is None:
        _con = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="spaghet",
            host="localhost",
            port="6666"
        )
    return _con.cursor()


def commit():
    _con.commit()


def close():
    _con.commit()
    _con.close()
