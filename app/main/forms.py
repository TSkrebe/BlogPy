
from app.models import User
from flask.ext.login import login_user
from flask.ext.wtf import Form
from wtforms import StringField, validators, PasswordField, SubmitField, BooleanField, TextAreaField


class LoginForm(Form):
    username = StringField("Username", validators=[validators.DataRequired()])
    password = PasswordField("Password", validators=[validators.DataRequired()])
    remember_me = BooleanField("Remember me", default=False)
    submit = SubmitField("Submit")

    def validate_on_submit(self):
        if not super(LoginForm, self).validate_on_submit():
            return False

        user = User.query.filter_by(username=self.username.data).first()
        if not user:
            return False

        if not user.verify_password(self.password.data):
            return False

        login_user(user, remember=self.remember_me.data)
        return True


class CommentForm(Form):
    name = StringField("Name", validators=[validators.data_required()])
    body_text = TextAreaField("Comment", validators=[validators.data_required()])
    submit = SubmitField("Submit")

