#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from functools import wraps

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import(
    check_password_hash, generate_password_hash
)

from flaskr.db import get_db

bp = Blueprint("auth", __name__, url_prefix = "/auth")

@bp.route("/register", methods=("GET", "POST"))
def register(): # 注册
    if (request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "需要用户名"
        elif not password:
            error = "需要密码"
        elif db.execute(
            "SELECT id FROM user WHERE username = ?", (username,)
        ).fetchone() is not None:
            error = "用户%s已被注册" % username

        if error == None:
            db.execute(
                "INSERT INTO user (username, password) VALUES (? ,?)",
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")

# 登录功能
@bp.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?" , (username,)
        ).fetchone()

        if user == None:
            error = "用户名不正确"
        elif not check_password_hash(user["password"], password):
            error = "密码错误"

        if error is None:
            session.clear()
            session["user_id"] = user["id"]
            return redirect(url_for("index"))

        flash(error)

    return render_template("auth/login.html")

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()

@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

def login_required(view):
    @wraps(view)
    def wrapped_view(**kwags):
        if g.user == None:
            return redirect(url_for("auth.login")) # url_for() 函数根据视图名称和发生成 URL 。

        return view(**kwags)

    return wrapped_view