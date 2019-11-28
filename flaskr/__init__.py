#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from flask import Flask

def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config = True) # 创建Flask实例
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    if (test_config == None):
        # load the instance configure,if it exists, when not testing
        app.config.from_pyfile("config.py", silent = True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/nmsl")
    def hello():
        return "NM$L"

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    app.add_url_rule("/", endpoint = "index")

    return app