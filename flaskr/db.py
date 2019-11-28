#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect( #g 是一个特殊对象，独立于每一个请求
            current_app.config["DATABASE"], # current_app 是另一个特殊对象，该对象指向处理请求的 Flask 应用。
            # 这里 使用了应用工厂，那么在其余的代码中就不会出现应用对象。
            # 当应用创建后，在处理 一个请求时， get_db 会被调用。这样就需要使用 current_app 。
            detect_types = sqlite3.PARSE_DECLTYPES
        )
        # sqlite3.connect() 建立一个数据库连接，
        # 该连接指向配置中的 DATABASE 指定的文件。
        # 这个文件现在还没有建立，后面会在初始化数据库的时候建立该文件。

        g.db.row_factory = sqlite3.Row # sqlite3.Row 告诉连接返回类似于字典的行，这样可以通过列名称来操作数据。

    return g.db

def close_db(e = None): # 通过检查 g.db 来确定连接是否已经建立。
    db = g.pop("db", None)

    if db != None:
        db.close()

def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as F:
        db.executescript(F.read().decode("utf8"))

@click.command("init-db")
@with_appcontext
def init_db_command():
    init_db()
    click.echo("Initialised the database")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)