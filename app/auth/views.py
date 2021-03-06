import os

from app import db
from app.auth.forms import PictureForm, PostForm, allowed_image_formats
from app.models import Post, Comment
from flask import Blueprint, url_for, abort, render_template, request, jsonify, current_app, flash
from flask.ext.login import login_required, logout_user
from werkzeug.utils import secure_filename, redirect

"""
    This bluprint is for routes that can be accessed only by the owner
"""

auth = Blueprint("auth", __name__, url_prefix="/auth")


@auth.before_request
@login_required
def before():
    pass


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@auth.route("/upload_pic", methods=["POST"])
def upload_image():
    form = PictureForm()
    if form.validate_on_submit():
        filename = secure_filename(form.picture.data.filename)
        form.picture.data.save(os.path.join(current_app.config["UPLOAD_DIRECTORY"], filename))
    return redirect(url_for("auth.panel"))


@auth.route("/post/<int:post_id>", methods=["GET", "POST"])
def update_post(post_id):

    # tries to update the model
    post = Post.query.get_or_404(post_id)
    post_form = PostForm(obj=post)
    if post_form.validate_on_submit():
        post.update(title=post_form.title.data,
                    body_text=post_form.body_text.data,
                    draft=post_form.draft.data)
        flash("Post updated")
        return redirect(url_for('auth.update_post', post_id=post_id))

    posts = Post.query.all()
    return render_template("auth/base.html", post_form=post_form,
                           picture_form=PictureForm(), posts=posts,
                           picture_names=get_image_list(), updates=True)


@auth.route("/post", methods=["GET", "POST"])
def panel():

    # renders a view for adding new post
    post_form = PostForm()
    if request.method == "POST":
        if post_form.validate():
            db.session.add(Post(title=post_form.title.data,
                                body_text=post_form.body_text.data,
                                draft=post_form.draft.data))
            flash("New post is added!!")
            return redirect(url_for('auth.panel'))
        else:
            flash("Something went wrong...")

    posts = Post.query.all()
    return render_template("auth/base.html", post_form=PostForm(),
                           picture_form=PictureForm(), posts=posts,
                           picture_names=get_image_list())


def get_image_list():
    files = os.listdir(current_app.config["UPLOAD_DIRECTORY"])
    for file in files:
        if file.lower().endswith(allowed_image_formats):
            yield file


@auth.route("/comment/delete/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    successful = Comment.query.filter_by(id=comment_id).delete()
    return jsonify(result=successful)


@auth.route("/post/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    successful = Post.query.filter_by(id=post_id).delete()
    return jsonify(result=successful)