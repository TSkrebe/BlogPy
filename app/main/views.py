from app.main.forms import LoginForm, CommentForm
from app.models import Post, Comment
from flask import Blueprint, render_template, request, url_for, redirect, session, \
    send_from_directory, current_app
from flask.ext.login import current_user


main = Blueprint("main", __name__)


@main.route("/")
def index():
    """:returns main page with DEFAULT_NUMBER_OF_POSTS"""
    items = Post.query.filter_by(draft=False).order_by(Post.created.desc()).limit(current_app.config["INITIAL_PAGE_LOAD"])
    return render_template("main/main.html", items=items, date_format=date_format)


@main.route("/about")
def about():
    return render_template("main/about.html")


@main.route("/projects")
def projects():
    return render_template("main/projects.html")


@main.route("/load_more_posts")
def load_more_posts():
    off = request.args.get("offset", 0, type=int)
    pages = request.args.get("pages", 0, type=int)
    items = Post.query.filter_by(draft=False).order_by(Post.created.desc()).offset(off).limit(pages)
    return render_template("main/load_more_posts.html", items=items, date_format=date_format)


@main.route("/search")
def search():
    text = request.args.get("text", "")
    if not text:
        next = request.referrer or url_for("main.index")
        return next
    posts = Post.query.filter_by(draft=False).filter(Post.body_text.like("%{}%".format(text))).all()
    return render_template("main/search.html", posts=posts, query=text)


@main.route("/post/<slug>", methods=["POST", "GET"])
def post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    comment_form = CommentForm()
    if comment_form.validate_on_submit():
        special = True if current_user.is_authenticated else False
        comment = Comment(name=comment_form.name.data,
                          body_text=comment_form.body_text.data,
                          special=special)
        session["name"] = comment.name
        post.comments.append(comment)
        return redirect(url_for("main.post", slug=slug, _anchor="write"))
    comment_form.name.data = session.get("name", "")
    comments = post.comments.order_by(Comment.timestamp.asc()).all()
    return render_template("main/post.html", post=post, date_format=date_format,
                           comments=comments, comment_form=comment_form)


@main.route("/image/<filename>")
def image(filename):
    return send_from_directory(current_app.config["UPLOAD_DIRECTORY"], filename)


@main.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        next = request.args.get("next")
        return redirect(next or url_for("auth.panel"))
    return render_template("main/login.html", form=form)


def date_format(date):
    return date.strftime("%d %B %Y")


@main.app_errorhandler(404)
def error404(error):
    return render_template("error404.html")