import click
from flask import current_app, g

import sys
sys.path.append('c:/users/aaron hofman/appdata/local/programs/python/python39/lib/site-packages')

import mysql.connector
def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
        user="ENTER_MYSQL_USER",
        password="ENTER_MYSQL_USER_PASSWORD",
        host="ENTER_HOST_NAME",
        port="ENTER_PORT_NUMBER",
        database="ENTER_DATABASE_NAME"
        )

    return g.db

def insert_edit_delete(mysql_command, inputs):
    cursor = g.db.cursor(dictionary=True)
    cursor.execute(mysql_command, inputs)
    g.db.commit()
    cursor.close()

def findUser(username, email):
    input = None
    if email is None:
        mysql_command = "SELECT * FROM user WHERE username=%s"
        input = username
    elif username is None:
        mysql_command = "SELECT * FROM user WHERE email=%s"
        input = email
    
    result = None
    try:
        cursor = g.db.cursor(dictionary=True)
        mysql_command = ""
        cursor.execute(mysql_command, (input,))
        result = cursor.fetchone()
        cursor.close()
    except:
        pass
    return result


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()
    print("initiate-part3")

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))
        print("initiate-part4")


@click.command('init-db')
def init_db_command():
    init_db()
    print("initiate-part2")
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    print("initiate")