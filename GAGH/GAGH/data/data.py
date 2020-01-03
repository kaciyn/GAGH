import sqlite3 as sql

from flask import g

# from https://flask.palletsprojects.com/en/0.12.x/patterns/sqlite3/#easy-querying
from GAGH import db_location, app


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sql.connect(db_location)
        g.db = db
        db.row_factory = sql.Row

    return db


@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()
