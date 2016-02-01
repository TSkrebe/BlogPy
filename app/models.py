import random
from datetime import datetime

from app import db, login_manager
from flask.ext.login import UserMixin
from slugify import slugify
from werkzeug.security import generate_password_hash, check_password_hash
import forgery_py


@login_manager.user_loader
def log_manager(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    real_name = db.Column(db.String(64))
    about_me = db.Column(db.TEXT)
    member_since = db.Column(db.DateTime, default=datetime.utcnow)

    verified = db.Column(db.Boolean, default=False)

    posts = db.relationship("Post", backref="author")

    def __init__(self, username, password, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()

    @property
    def password(self):
        raise PermissionError("No permission to look at the password")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_users():
        user = User(username="johny", password="best", verified=True)
        db.session.add(user)


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256))
    body_text = db.Column(db.TEXT)
    created = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_update = db.Column(db.DateTime)
    draft = db.Column(db.Boolean, default=False, index=True)
    slug = db.Column(db.String(260), unique=True)

    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    comments = db.relationship("Comment", backref="post",
                               lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.slug = Post.find_unique_slug(self.title)

    def update(self, **kwargs):
        self.last_update = datetime.utcnow()
        self.title = kwargs["title"]
        self.slug = Post.find_unique_slug(self.title)
        self.body_text = kwargs["body_text"]
        self.draft = kwargs["draft"]

    @staticmethod
    def find_unique_slug(title):
        slug = slugify(title)
        if Post.query.filter_by(slug=slug).first() is None:
            return slug
        nr = 1
        while Post.query.filter_by(slug='{}-{}'.format(slug, nr)).first() is not None:
            nr += 1
        return '{}-{}'.format(slug, nr)

    @staticmethod
    def generate_posts():
        user = User.query.first()
        for x in range(20):
            post = Post(title=forgery_py.lorem_ipsum.sentence(),
                        body_text=forgery_py.lorem_ipsum.paragraphs(4),
                        created=forgery_py.date.date(),
                        author=user)
            db.session.add(post)


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    # comment by a registered user
    special = db.Column(db.Boolean)
    body_text = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    disabled = db.Column(db.Boolean, default=False)

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @staticmethod
    def generate_comments():
        count = Post.query.count()
        for x in range(100):
            sp = True if x % 10 == 0 else False
            post_to = Post.query.offset(random.randint(0, count-1)).first()
            comment = Comment(name=forgery_py.name.full_name(),
                              special=sp,
                              body_text=forgery_py.lorem_ipsum.paragraph())
            post_to.comments.append(comment)
            db.session.add(post_to)
