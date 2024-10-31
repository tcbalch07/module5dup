import pymysql
from flask import g

def get_db():
    """Get a database connection, establishing a new one if necessary."""
    if 'db' not in g or not is_connection_open(g.db):
        g.db = pymysql.connect(
            host='otmaa16c1i9nwrek.cbetxkdyhwsb.us-east-1.rds.amazonaws.com',
            user='pvv0mxhegmpeibnz',
            password='u53cu6cnifzx2cue',
            database='jjkt43uxx702xb76',
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.db

def is_connection_open(conn):
    """Check if the connection is open and reconnect if necessary."""
    try:
        conn.ping(reconnect=True)
        return True
    except:
        return False

def close_db(exception=None):
    """Close the database connection if it exists."""
    db = g.pop('db', None)
    if db is not None and not db._closed:
        db.close()
