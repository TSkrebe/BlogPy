import os

from app import db
from app.auth.forms import PictureForm, PostForm
from app.models import Post, Comment
from flask import Blueprint, url_for, abort, render_template, request, jsonify, current_app
from flask.ext.login import login_required, logout_user, current_user
from werkzeug.utils import secure_filename, redirect

"""
    This bluprint is for routes that can be accessed only by the owner
"""

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.before_request
@login_required
def before():
    pass


@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index'))


@auth.route("/upload_pic", methods=["POST"])
def upload_pic():
    form = PictureForm()
    if form.validate_on_submit():
        filename = secure_filename(form.picture.data.filename)
        form.picture.data.save(os.path.join(current_app.config["UPLOAD_DIRECTORY"], filename))
    return redirect(url_for('auth.panel'))


@auth.route("/merge_post/<integer:post_id>", methods=["POST"])
def update_add_post(post_id):
    post = Post.query.get(post_id)
    if post is not None and post.author != current_user:
        abort(403)
    if post_id < -1:
        return redirect(url_for('auth.panel'))

    post_form = PostForm()
    if post_form.validate_on_submit():
        if post is None:
            new_post = Post(title=post_form.title.data,
                            body_text=post_form.body_text.data,
                            draft=post_form.draft.data,
                            author=current_user._get_current_object())
            db.session.add(new_post)
            db.session.commit()
            post_id = new_post.id
        else:
            post.update(title=post_form.title.data,
                        body_text=post_form.body_text.data,
                        draft=post_form.draft.data)
            db.session.merge(post)
    return redirect(url_for('auth.panel', post_id=post_id))


@auth.route("/panel/", defaults={'post_id': -1})
@auth.route("/panel/<integer:post_id>")
def panel(post_id):
    post = Post.query.get(post_id)
    if post is not None and post.author != current_user:
        abort(403)
    if post_id < -1:
        return redirect(url_for('auth.panel'))
    post_form = PostForm()
    if post is not None:
        post_form.title.data = post.title
        post_form.body_text.data = post.body_text
        post_form.draft.data = post.draft
    posts = Post.query.all()
    picture_names = os.listdir(current_app.config["UPLOAD_DIRECTORY"])
    return render_template('auth/panel.html', post_form=post_form,
                           picture_form=PictureForm(), posts=posts,
                           picture_names=picture_names, post_id=post_id)


@auth.route("/comment/delete/<int:comment_id>", methods=["POST"])
def delete_comment(comment_id):
    successful = Comment.query.filter_by(id=comment_id).delete()
    return jsonify(result=successful)


@auth.route("/post/delete/<int:post_id>", methods=["POST"])
def delete_post(post_id):
    Post.query.filter_by(id=post_id).delete()
    return redirect(request.args.get('next', '') or
                    request.referrer or
                    url_for('main.index'))
