from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
import sqlalchemy as sa
from app import db
from app.models import User

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    summary = TextAreaField('Summary')
    body = TextAreaField('Body', validators=[DataRequired()])
    submit = SubmitField('Publish')