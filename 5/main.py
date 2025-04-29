#!/usr/bin/env python3
import secrets

import click
import sqlite3
import prettytable
import random
import hashlib
from prettytable import PrettyTable


@click.group()
def cli():
    ...


db = sqlite3.connect('db.sqlite')
db.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT, salt TEXT)')

def get_hash(s: str) -> str:
    m = hashlib.sha256()
    m.update(s.encode())
    return m.hexdigest()


@cli.command()
@click.argument('username', type=str)
@click.argument('password', type=str)
def signup(username: str, password: str):
    salt = secrets.token_hex(16)
    hashed_password = get_hash(salt + password)
    db.execute(
        'INSERT INTO users (username, password, salt) VALUES (?, ?, ?)', (username, hashed_password, salt))
    db.commit()

@cli.command()
@click.argument('username', type=str)
@click.argument('password', type=str)
def login(username: str, password: str):
    hashed_password, salt = db.execute('SELECT password, salt FROM users WHERE username = ?', (username,)).fetchone()
    if hashed_password == get_hash(salt + password):
        print('Login successful')
    else:
        print('Login failed')

@cli.command()
def dump():
    all_users = db.execute('SELECT * FROM users').fetchall()
    t = PrettyTable()
    t.field_names = ['id', 'username', 'password', 'salt']
    t.add_rows(all_users)
    print(t)

if __name__ == '__main__':
    cli()