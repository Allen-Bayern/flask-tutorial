#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Blueprint, flash, g, redirect, render_template, request, url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)

# 索引
@bp.route("/")
def index():
    db = get_db()
    posts = db.execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " ORDER BY created DESC"
    ).fetchall()
    return render_template( "blog/index.html",posts = posts)


# 创建
@bp.route("/create", methods = ("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "请输入标题"
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (title, body, author_id)"
                " VALUES (?, ?, ?)",
                (title, body, g.user["id"])
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")

'''
update 和 delete 视图都需要通过 id 来获取一个 post ，并且检查作者与登录用户是否一致。
为避免重复代码，可以写一个函数来获取 post ，并在每个视图中调用它。
'''

def get_post(id, check_author = True):
    #  check_author 参数的作用是函数可以用于在不检查作者的情况下获取一个 post
    post = get_db().execute(
        "SELECT p.id, title, body, created, author_id, username"
        " FROM post p JOIN user u ON p.author_id = u.id"
        " WHERE p.id = ?",
        (id, )
    ).fetchone()

    if post == None:
        abort(404, "Post id %d does not exist"%id)

    if check_author and post["author_id"] != g.user["id"]:
        abort(403)

    return post

# 更新
@bp.route("/<int:id>/update", methods = ("GET", "PODT"))
@login_required
def update(id):
    post = get_post(id)

    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "需要标题"

        if error != None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?",
                (title, body, id)
            )
            db.commit()
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post = post)

# 删除
@bp.route("/<int:id>/delete", methods = ("POST",))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute("DELETE FROM post WHERE id = ?", (id, ))
    db.commmit()
    return redirect(url_for("blog.index"))