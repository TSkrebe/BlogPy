from flask.ext.pagedown.fields import PageDownField
from flask.ext.wtf import Form
from flask.ext.wtf.file import FileField, FileRequired, FileAllowed

from wtforms import SubmitField, BooleanField, StringField, validators, HiddenField

allowed_image_formats = ("png", "jpg", "gif", "jpeg")


class PostForm(Form):
    id = HiddenField("Id")
    title = StringField("Title", validators=[validators.Length(max=256), validators.data_required()])
    body_text = PageDownField("Your post", validators=[validators.data_required()])
    draft = BooleanField("Draft", default=False)
    submit = SubmitField("Submit")


class PictureForm(Form):
    picture = FileField("File", validators=[FileRequired(), FileAllowed(allowed_image_formats)])
    submit = SubmitField("Upload")
